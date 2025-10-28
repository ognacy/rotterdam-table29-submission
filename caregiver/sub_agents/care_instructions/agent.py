
from . import prompt
from google.adk.agents import Agent

from caregiver.tools.care_instructions import get_care_instructions

care_instructions_agent = Agent(
    model="gemini-2.5-flash",
    name="care_instructions_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="Given a question on care instructions for the Patient, inform the Caregiver",
    tools=[get_care_instructions]
)
