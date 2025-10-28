
from . import prompt
from google.adk.agents import Agent

record_meds_agent = Agent(
    model="gemini-2.5-flash",
    name="record_meds_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="If the Caregiver wants to register which meds the Patient took (or skipped) and leave any related comments, record them"
)
