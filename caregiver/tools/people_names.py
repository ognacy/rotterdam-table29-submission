"""This tool returns the list of person names:

  - that of other caregivers
  - that of the parents
  - that of the patient

  So that the bot can understand people references in utterances such as "Leave a note for Bob" - 
  is Bob a parent? Another caregiver? 

  Returns:
      _type_: _description_
"""

from google.adk.tools import FunctionTool

SAMPLE_SCENARIO = {
  "caregiver_names": ["Derek", "Carol", "Bob"],
  "parent_names": ["Alfred", "Rose"],
  "patient": "John"
}

async def get_people_names(patient: str) -> dict:
  return SAMPLE_SCENARIO

people_names_tool = FunctionTool(get_people_names)
