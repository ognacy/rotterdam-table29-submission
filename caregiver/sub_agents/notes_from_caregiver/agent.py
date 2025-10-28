
from . import prompt
from google.adk.agents import Agent

from caregiver.tools.record_caregiver_note import record_note_tool, edit_note_tool, delete_note_tool


notes_from_caregiver_agent = Agent(
    model="gemini-2.5-flash",
    name="notes_from_caregiver_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="When the Caregiver wants to record a general note pertaining the Patient, capture it",
    tools=[record_note_tool, edit_note_tool, delete_note_tool]
)
