from google.adk.tools import FunctionTool

SAMPLE_RESPONSE_RECORD = {
  "id_of_note_just_recorded": "1"
}

SAMPLE_RESPONSE_EDIT = "OK"

SAMPLE_RESPONSE_DELETE = "OK"


async def record_note(note: str) -> dict:
  """Records a note provided by the caregiver.

  Args:
      note (str): text of the note

  Returns:
      dict: _description_
  """
  return SAMPLE_RESPONSE_RECORD

async def edit_note(note_id: str, corrected_note: str) -> str:
  """Edits a note recorded earlier by the caregiver. 

  Args:
      note_id (str): id of the note being edited
      corrected_note (str): new text of the note

  Returns:
      "OK" in case of success, "Error" in case of an error. 
  """
  return SAMPLE_RESPONSE_RECORD

async def delete_note(note_id: str) -> dict:
  """Deletes a note that the caregiver just submitted 

  Args:
      note_id (str): id of the earlier submitted note

  Returns:
      dict: _description_
  """
  return SAMPLE_RESPONSE_RECORD


record_note_tool = FunctionTool(record_note)
edit_note_tool = FunctionTool(edit_note)
delete_note_tool = FunctionTool(delete_note)
