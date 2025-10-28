
from . import prompt
from google.adk.agents import Agent

from caregiver.shared_libraries import constants
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext


from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

from caregiver.tools.shift_summary import shift_start_summary_tool
from caregiver.tools.garmin_activity import garmin_daily_sleep

def _remember_we_gave_the_daily_update(callback_context: CallbackContext):
    callback_context.state.update({"gave_shift_summary_today": "True"})    


shift_start_agent = Agent(
    model="gemini-2.5-flash",
    name="shift_start_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="When the Caregiver starts their shift, " \
    "inform them about anything relevant to their shift - what happened " \
    "recently, what is planned, and if there any notes from the " \
    "Parents or new care instructions",
    after_agent_callback=_remember_we_gave_the_daily_update,
    tools=[
        shift_start_summary_tool, 
        garmin_daily_sleep]
)
