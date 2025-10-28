import asyncio
from google.cloud import firestore

async def get_care_instructions(patient_name: str):
    db = firestore.AsyncClient(database="default")
    doc_ref = db.collection("care-instructions").document(patient_name)
    doc = await doc_ref.get()
    if doc.exists:
        print("Retrieved care instructions")
        return doc.to_dict().get("instructions", [])
    return []
