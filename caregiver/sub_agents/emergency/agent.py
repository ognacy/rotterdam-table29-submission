
from . import prompt
from google.adk.agents import Agent

emergency_agent = Agent(
    model="gemini-2.5-flash",
    name="emergency_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="In case of emergency, notify others and log the problem"
)
