# Caregiver Agent

This directory contains an agent that acts as a caregiver.

## Responsibilities

The caregiver agent is responsible for logging information about the patient, including:

*   Activities
*   Meals
*   Medications
*   Notes

This information is logged using the Patient Logger Agent. The agent is composed of sub-agents that are responsible for handling specific tasks.

## Sub-agents

The `sub_agents/` directory contains the following sub-agents:

*   `all_other_matters`: Handles all other matters that are not covered by the other sub-agents.
*   `care_instructions`: Handles care instructions.
*   `emergency`: Handles emergency situations.
*   `notes_from_caregiver`: Handles notes from the caregiver.
*   `notes_from_parents`: Handles notes from the parents.
*   `record_activites`: Records patient activities.
*   `record_meals`: Records patient meals.
*   `record_meds`: Records patient medications.
*   `shift_start_report`: Generates a report at the start of a shift.

## Tools

The `tools/` directory contains tools that are used by the agent, such as:

*   `memory.py`: Provides a memory for the agent.
*   `people_names.py`: Manages people's names.
*   `record_caregiver_note.py`: Records a note from the caregiver.
*   `record_meds.py`: Records medications.
*   `shift_summary.py`: Generates a shift summary.

## Profiles

The `profiles/` directory contains profiles that can be used to configure the agent.
