
from . import prompt
from google.adk.agents import Agent

record_meals_agent = Agent(
    model="gemini-2.5-flash",
    name="record_meals_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="If the Caregiver wants to register what the Patient ate and leave any related comments, record it"
)
