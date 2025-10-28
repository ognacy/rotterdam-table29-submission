from google.cloud import datastore
from datetime import datetime

def read_log(log_id: str) -> dict:
    """Reads a patient log from Datastore given a log ID.

    Args:
        log_id: The ID of the log to read.

    Returns:
        A dictionary representing the log.
    """
    client = datastore.Client(database='patient-logs')
    key = client.key('PatientLog', int(log_id))
    entity = client.get(key)
    return entity

def load_all_logs(patient_id: str, limit: int = 10, offset: int = 0) -> list[dict]:
    """Loads logs for a given patient ID from Datastore, sorted by most recent first.

    Args:
        patient_id: The ID of the patient to load logs for.
        limit: The maximum number of logs to return. Defaults to 10.
        offset: The number of logs to skip. Defaults to 0.

    Returns:
        A list of dictionaries representing the logs.
    """
    client = datastore.Client(database='patient-logs')
    query = client.query(kind='PatientLog')
    query.add_filter('patient_id', '=', patient_id)
    query.order = ['-timestamp']
    logs = list(query.fetch(limit=limit, offset=offset))
    return logs

def create_log(patient_id: str, caregiver_name: str, caregiver_surname: str, relationship: str, summary: str) -> str:
    """Creates a new patient log entry in Datastore.

    Args:
        patient_id: The ID of the patient.
        caregiver_name: The first name of the caregiver.
        caregiver_surname: The surname of the caregiver.
        relationship: The relationship between the caregiver and the patient.
        summary: The summary of the interview.

    Returns:
        The ID of the newly created log entry as a string.
    """
    client = datastore.Client(database='patient-logs')
    key = client.key('PatientLog')
    entity = datastore.Entity(key=key)
    entity.update({
        'patient_id': patient_id,
        'caregiver_name': caregiver_name,
        'caregiver_surname': caregiver_surname,
        'relationship': relationship,
        'summary': summary,
        'timestamp': datetime.utcnow()
    })
    client.put(entity)
    return str(entity.key.id)

def create_patient_profile(patient_id: str, name: str, surname: str, email: str, phone: str, situation: str) -> str:
    """Creates a new patient profile in Datastore.

    Args:
        patient_id: The unique ID of the patient.
        name: The first name of the patient.
        surname: The surname of the patient.
        email: The contact email of the patient.
        phone: The contact phone number of the patient.
        situation: A brief description of the patient's special situation.

    Returns:
        A string confirming the creation of the patient profile.
    """
    client = datastore.Client(database='patient-logs')
    key = client.key('PatientProfile', patient_id)
    entity = datastore.Entity(key=key)
    entity.update({
        'name': name,
        'surname': surname,
        'email': email,
        'phone': phone,
        'situation': situation,
        'registration_date': datetime.utcnow()
    })
    client.put(entity)
    return f"Successfully created profile for patient {name} {surname} with ID {patient_id}."

def check_patient_exists(patient_id: str) -> bool:
    """Checks if a patient profile exists in Datastore.

    Args:
        patient_id: The unique ID of the patient to check.

    Returns:
        True if the patient exists, False otherwise.
    """
    client = datastore.Client(database='patient-logs')
    key = client.key('PatientProfile', patient_id)
    entity = client.get(key)
    return entity is not None

def delete_patient_profile(patient_id: str) -> str:
    """Deletes a patient's profile and all their associated logs from Datastore.

    Args:
        patient_id: The ID of the patient whose data will be deleted.

    Returns:
        A string confirming the deletion of all patient data.
    """
    client = datastore.Client(database='patient-logs')

    # Delete all logs for the patient
    log_query = client.query(kind='PatientLog')
    log_query.add_filter('patient_id', '=', patient_id)
    log_query.keys_only()
    log_keys = [entity.key for entity in log_query.fetch()]
    
    logs_deleted_count = 0
    if log_keys:
        client.delete_multi(log_keys)
        logs_deleted_count = len(log_keys)

    # Delete the patient profile
    profile_key = client.key('PatientProfile', patient_id)
    client.delete(profile_key)

    return f"Successfully deleted profile and {logs_deleted_count} log(s) for patient ID {patient_id}."

def get_patient_profile(patient_id: str) -> dict:
    """Fetches a patient profile from Datastore.

    Args:
        patient_id: The unique ID of the patient to fetch.

    Returns:
        A dictionary representing the patient profile, or None if not found.
    """
    client = datastore.Client(database='patient-logs')
    key = client.key('PatientProfile', patient_id)
    entity = client.get(key)
    return entity