
from . import prompt
from google.adk.agents import Agent

record_activities_agent = Agent(
    model="gemini-2.5-flash",
    name="record_activites_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="If the caregiver wants to inform physical activities of the Patient, record it"
)
