from google.adk.tools import FunctionTool

SAMPLE_RESPONSE_RECORD = {
  "id_of_med_note_just_recorded": "1"
}

SAMPLE_RESPONSE_EDIT = "OK"

SAMPLE_RESPONSE_DELETE = "OK"


async def record_med_note(note: str) -> dict:
  """Records a medicine related note provided by the caregiver.
  Stores it in the shift record. 

  Args:
      note (str): text of the note

  Returns:
      dict: _description_
  """
  return SAMPLE_RESPONSE_RECORD

async def edit_med_note(note_id: str, corrected_note: str) -> str:
  """Edits a medicines note recorded earlier by the caregiver. 
  Edits the shift record. 

  Args:
      note_id (str): id of the note being edited
      corrected_note (str): new text of the note

  Returns:
      "OK" in case of success, "Error" in case of an error. 
  """
  return SAMPLE_RESPONSE_RECORD

async def delete_med_note(note_id: str) -> dict:
  """Deletes a note that the caregiver just submitted 
  Deletes from the shift record 

  Args:
      note_id (str): id of the earlier submitted note

  Returns:
      dict: _description_
  """
  return SAMPLE_RESPONSE_RECORD


record_medicine_tool = FunctionTool(record_med_note)
edit_medicine_tool = FunctionTool(edit_med_note)
delete_medicine_tool = FunctionTool(delete_med_note)
