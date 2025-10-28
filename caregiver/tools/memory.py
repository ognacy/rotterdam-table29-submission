from datetime import datetime
import json
import os
from typing import Dict, Any

from caregiver.shared_libraries import constants
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

SAMPLE_SCENARIO_PATH = os.getenv(
    "CAREGIVER_SCENARIO", "caregiver/profiles/scenario-empty.json"
)

def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Setting the initial session state given a JSON object of states.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.
    """
    if constants.SYSTEM_TIME not in target:
        target[constants.SYSTEM_TIME] = str(datetime.now())

    if constants.STATE_INITIALIZED not in target:
        target[constants.STATE_INITIALIZED] = True

        target.update(source)


def _load_initial_state(callback_context: CallbackContext):
    """
    Sets up the initial state.
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is contructed.

    Args:
        callback_context: The callback context.
    """    
    data = {}
    import os

    print(os.getcwd())
    with open(SAMPLE_SCENARIO_PATH, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    _set_initial_states(data["state"], callback_context.state)