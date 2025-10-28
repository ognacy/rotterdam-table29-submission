
from . import prompt
from google.adk.agents import Agent

notes_from_parents_agent = Agent(
    model="gemini-2.5-flash",
    name="notes_from_parents",
    instruction=prompt.SUB_AGENT_INSTR,
    description="If Caregiver asks about any recent notes concerning the patient care, answer the question"
)
