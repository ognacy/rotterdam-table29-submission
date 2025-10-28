
from . import prompt
from google.adk.agents import Agent

all_other_matters_agent = Agent(
    model="gemini-2.5-flash",
    name="all_other_matters_agent",
    instruction=prompt.SUB_AGENT_INSTR,
    description="Given a general question not covered by the specialized agents, provide assistance/give answer"
)
