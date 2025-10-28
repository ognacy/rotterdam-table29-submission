from caregiver import prompt
from google.adk.agents import Agent

from caregiver.sub_agents.all_other_matters.agent import all_other_matters_agent
from caregiver.sub_agents.care_instructions.agent import care_instructions_agent
from caregiver.sub_agents.notes_from_caregiver.agent import notes_from_caregiver_agent
from caregiver.sub_agents.record_activites.agent import record_activities_agent
from caregiver.sub_agents.record_meals.agent import record_meals_agent
from caregiver.sub_agents.record_meds.agent import record_meds_agent
from caregiver.sub_agents.shift_start_report.agent import shift_start_agent

from caregiver.tools.memory import _load_initial_state
from caregiver.tools.people_names import get_people_names

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="A Caregiver helper utilizing multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        all_other_matters_agent,
        care_instructions_agent,
        notes_from_caregiver_agent,
        record_activities_agent,
        record_meals_agent,
        record_meds_agent,
        shift_start_agent
    ],
    before_agent_callback=_load_initial_state, 
    tools=[get_people_names]
)