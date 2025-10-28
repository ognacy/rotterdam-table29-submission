# tools/garmin_sleep_wrapper.py
import asyncio
import os
from typing import Dict, Any, Optional

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# --- New: Google Secret Manager (async) ---
# Tries the native async client; falls back to thread-executed sync client if needed.
try:
    from google.cloud.secretmanager_v1 import SecretManagerServiceAsyncClient as _SMAsyncClient
    _HAS_NATIVE_ASYNC_SM = True
except Exception:  # pragma: no cover
    from google.cloud.secretmanager_v1 import SecretManagerServiceClient as _SMSyncClient
    _HAS_NATIVE_ASYNC_SM = False

# Cache for the secret & toolset
_garth_toolset: Optional[MCPToolset] = None
_daily_sleep_tool = None
_garth_token: Optional[str] = None

# Helper: resolve project id from common env vars
def _resolve_project_id() -> Optional[str]:
    return (
        os.environ.get("GOOGLE_CLOUD_PROJECT")
        or os.environ.get("GCP_PROJECT")
        or os.environ.get("PROJECT_ID")
    )

async def _get_secret_async(
    secret_id: str,
    *,
    project_id: Optional[str] = None,
    fully_qualified_name: Optional[str] = None,
) -> str:
    """
    Retrieve a secret value from Google Secret Manager asynchronously.

    You can optionally pass a fully qualified name:
      projects/{PROJECT}/secrets/{SECRET}/versions/{VERSION}

    Otherwise, we resolve {PROJECT} from env and use version 'latest'.
    """
    # Allow power users to override with a fully qualified name via env.
    if fully_qualified_name is None:
        # Also permit overriding via env var (useful in multi-project setups)
        fully_qualified_name = os.environ.get("GARMIN_SECRET_NAME")

    if fully_qualified_name is None:
        pid = project_id or _resolve_project_id()
        if not pid:
            raise RuntimeError(
                "Project ID is not set. Please set one of "
                "GOOGLE_CLOUD_PROJECT / GCP_PROJECT / PROJECT_ID, "
                "or set GARMIN_SECRET_NAME to a fully-qualified secret name."
            )
        fully_qualified_name = f"projects/{pid}/secrets/{secret_id}/versions/latest"

    if _HAS_NATIVE_ASYNC_SM:
        client = _SMAsyncClient()
        resp = await client.access_secret_version(name=fully_qualified_name)
        return resp.payload.data.decode("utf-8")

    # Fallback: run the sync client in a worker thread to avoid blocking the loop
    def _blocking_fetch() -> str:
        client = _SISyncClient()  # Typo fix below
        resp = client.access_secret_version(name=fully_qualified_name)
        return resp.payload.data.decode("utf-8")

    # NOTE: fix: correct class name for sync client
    # We define here to avoid NameError above.
    from google.cloud.secretmanager_v1 import SecretManagerServiceClient as _SISyncClient  # noqa: E402

    return await asyncio.to_thread(_blocking_fetch)

async def _get_garmin_token() -> str:
    """Fetch and cache the Garmin token from Secret Manager."""
    global _garth_token
    if _garth_token:
        return _garth_token

    # Secret is already created and called 'garmin-token'
    token = await _get_secret_async("garmin-token")
    if not token:
        raise RuntimeError("garmin-token resolved to an empty value in Secret Manager.")
    _garth_token = token
    return _garth_token

async def _ensure_daily_sleep_tool():
    global _garth_toolset, _daily_sleep_tool
    if _daily_sleep_tool:
        return _daily_sleep_tool

    garth_token = await _get_garmin_token()

    _garth_toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uvx",
                args=["garth-mcp-server"],
                env={
                    # Inject the token fetched from Secret Manager
                    "GARTH_TOKEN": garth_token
                },
            ),
        ),
        tool_filter=["daily_sleep"],  # only fetch what we need
    )

    # Get ADK-wrapped MCP tools
    tools = await _garth_toolset.get_tools()
    for t in tools:
        if t.name == "daily_sleep":
            _daily_sleep_tool = t
            break
    if not _daily_sleep_tool:
        raise RuntimeError("daily_sleep tool not found on MCP server")
    return _daily_sleep_tool

async def garmin_daily_sleep(tool_context: ToolContext, end_date: str, days: int = 2) -> Dict[str, Any]:
    print(f"checking sleep for {end_date} and limit {days} ")

    # Map wrapper args -> MCP tool args
    args = {"days": int(days)}
    if end_date:
        args["end_date"] = end_date  # YYYY-MM-DD

    tool = await _ensure_daily_sleep_tool()

    # Invoke the MCP tool directly. BaseTool.run_async is the public call surface.
    # We pass the current ToolContext so logs/telemetry stay wired up.
    result = await tool.run_async(tool_context=tool_context, args=args)

    # FunctionTool must return a dict. Wrap result if needed.
    return {"result": result}
