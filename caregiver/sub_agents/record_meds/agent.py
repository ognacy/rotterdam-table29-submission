
from . import prompt
from google.adk.agents import Agent

from caregiver.tools.record_meds import record_medicine_tool, edit_medicine_tool, delete_medicine_tool

record_meds_agent = Agent(
    model="gemini-2.5-flash",
    name="record_meds_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="If the Caregiver wants to register which meds the Patient took (or skipped) and leave any related comments, record them", 
    tools=[record_medicine_tool, edit_medicine_tool, delete_medicine_tool]
)
