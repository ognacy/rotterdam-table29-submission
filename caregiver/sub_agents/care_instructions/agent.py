
from . import prompt
from google.adk.agents import Agent

care_instructions_agent = Agent(
    model="gemini-2.5-flash",
    name="care_instructions_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="Given a question on care instructions for the Patient, inform the Caregiver"
)
