"""Agent tools for Firestore Native with logging.

These tools can be used by agents to save and retrieve data from Firestore.
All operations are logged for debugging.
"""

from typing import Dict, Any, Optional
import logging
from team29.firestore_native_service import get_firestore_native_service

logger = logging.getLogger('FirestoreAgentTools')


# ========== FOOD PREFERENCES ==========

def save_patient_food_preferences(
    patient_id: str,
    likes: str,
    dislikes: str,
    allergies: str = '',
    notes: str = ''
) -> str:
    """
    Save food preferences for a patient.

    Args:
        patient_id: Patient identifier (e.g., 'John')
        likes: Comma-separated list of liked foods
        dislikes: Comma-separated list of disliked foods
        allergies: Comma-separated list of allergies (optional)
        notes: Additional dietary notes (optional)

    Returns:
        Confirmation message

    Example:
        save_patient_food_preferences(
            patient_id='John',
            likes='chicken, vegetables, rice',
            dislikes='spicy food, seafood',
            allergies='peanuts',
            notes='Prefers smaller meals'
        )
    """
    logger.info(f"🔧 Tool called: save_patient_food_preferences")
    logger.info(f"   Patient ID: {patient_id}")
    logger.info(f"   Likes: {likes}")
    logger.info(f"   Dislikes: {dislikes}")
    logger.info(f"   Allergies: {allergies}")
    logger.info(f"   Notes: {notes}")

    service = get_firestore_native_service()

    # Parse comma-separated lists
    preferences = {
        'likes': [item.strip() for item in likes.split(',') if item.strip()],
        'dislikes': [item.strip() for item in dislikes.split(',') if item.strip()],
        'allergies': [item.strip() for item in allergies.split(',') if item.strip()] if allergies else [],
        'notes': notes.strip() if notes else '',
        'type': 'dietary_preferences'
    }

    # Save to Firestore
    service.save_food_preferences(patient_id, preferences)

    result = f"""✅ Food preferences saved for {patient_id}!

Likes: {', '.join(preferences['likes'])}
Dislikes: {', '.join(preferences['dislikes'])}
Allergies: {', '.join(preferences['allergies']) if preferences['allergies'] else 'None'}
Notes: {preferences['notes'] if preferences['notes'] else 'None'}

This information is now stored in Firestore and accessible to all agents."""

    logger.info(f"✅ Tool completed successfully")
    return result


def get_patient_food_preferences(patient_id: str) -> str:
    """
    Get food preferences for a patient.

    Args:
        patient_id: Patient identifier

    Returns:
        Formatted food preferences
    """
    logger.info(f"🔧 Tool called: get_patient_food_preferences")
    logger.info(f"   Patient ID: {patient_id}")

    service = get_firestore_native_service()
    preferences = service.get_food_preferences(patient_id)

    if not preferences:
        result = f"No food preferences found for {patient_id}."
        logger.warning(f"⚠️  No preferences found")
        return result

    result = f"""🍽️ Food Preferences for {patient_id}:

✅ LIKES:
{chr(10).join(f'   • {item}' for item in preferences.get('likes', []))}

❌ DISLIKES:
{chr(10).join(f'   • {item}' for item in preferences.get('dislikes', []))}

⚠️ ALLERGIES:
{chr(10).join(f'   • {item}' for item in preferences.get('allergies', [])) if preferences.get('allergies') else '   • None'}

📝 NOTES:
   {preferences.get('notes', 'None')}
"""

    logger.info(f"✅ Tool completed successfully")
    return result


# ========== CARE INSTRUCTIONS ==========

def add_patient_care_instruction(patient_id: str, instruction: str) -> str:
    """
    Add a care instruction for a patient.

    Args:
        patient_id: Patient identifier
        instruction: The instruction to add

    Returns:
        Confirmation message
    """
    logger.info(f"🔧 Tool called: add_patient_care_instruction")
    logger.info(f"   Patient ID: {patient_id}")
    logger.info(f"   Instruction: {instruction}")

    service = get_firestore_native_service()
    service.add_care_instruction(patient_id, instruction)

    result = f"""✅ Care instruction added for {patient_id}!

Instruction: "{instruction}"

This instruction is now stored in Firestore and visible to all caregivers."""

    logger.info(f"✅ Tool completed successfully")
    return result


def get_patient_care_instructions(patient_id: str) -> str:
    """
    Get all care instructions for a patient.

    Args:
        patient_id: Patient identifier

    Returns:
        Formatted care instructions
    """
    logger.info(f"🔧 Tool called: get_patient_care_instructions")
    logger.info(f"   Patient ID: {patient_id}")

    service = get_firestore_native_service()
    instructions = service.get_care_instructions(patient_id)

    if not instructions:
        result = f"No care instructions found for {patient_id}."
        logger.warning(f"⚠️  No instructions found")
        return result

    result = f"""📋 Care Instructions for {patient_id}:

"""
    for i, instruction in enumerate(instructions, 1):
        result += f"{i}. {instruction}\n"

    logger.info(f"✅ Tool completed successfully - Found {len(instructions)} instructions")
    return result


# ========== FOOD INTAKE (Daily) ==========

def save_patient_food_intake(
    patient_id: str,
    shift_id: str,
    meals: str
) -> str:
    """
    Save daily food intake for a patient.

    Args:
        patient_id: Patient identifier
        shift_id: Shift identifier (e.g., 'shift-897')
        meals: Description of meals consumed

    Returns:
        Confirmation message
    """
    logger.info(f"🔧 Tool called: save_patient_food_intake")
    logger.info(f"   Patient ID: {patient_id}")
    logger.info(f"   Shift ID: {shift_id}")
    logger.info(f"   Meals: {meals}")

    service = get_firestore_native_service()
    doc_id = service.save_food_intake(patient_id, shift_id, meals)

    result = f"""✅ Food intake recorded for {patient_id}!

Shift: {shift_id}
Meals: {meals}

Saved to: food/{doc_id}"""

    logger.info(f"✅ Tool completed successfully")
    return result


# ========== GENERIC SAVE ==========

def save_to_firestore_collection(
    collection: str,
    document_id: str,
    data: str
) -> str:
    """
    Generic tool to save data to any Firestore collection.

    Args:
        collection: Collection name (e.g., 'food-preferences', 'care-instructions')
        document_id: Document ID (usually patient ID)
        data: JSON string of data to save

    Returns:
        Confirmation message
    """
    logger.info(f"🔧 Tool called: save_to_firestore_collection")
    logger.info(f"   Collection: {collection}")
    logger.info(f"   Document ID: {document_id}")
    logger.info(f"   Data: {data}")

    import json
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        # If not JSON, treat as a simple value
        data_dict = {'value': data}

    service = get_firestore_native_service()
    service.save_to_collection(collection, document_id, data_dict)

    result = f"""✅ Data saved to Firestore!

Collection: {collection}
Document ID: {document_id}
Fields: {list(data_dict.keys())}"""

    logger.info(f"✅ Tool completed successfully")
    return result


# ========== MONITORING ==========

def list_firestore_collections() -> str:
    """
    List all collections in the Firestore database.

    Returns:
        List of collection names
    """
    logger.info(f"🔧 Tool called: list_firestore_collections")

    service = get_firestore_native_service()
    collections = service.list_all_collections()

    result = f"""📂 Firestore Collections ({len(collections)} total):

"""
    for collection in collections:
        result += f"   • {collection}\n"

    logger.info(f"✅ Tool completed successfully")
    return result


def check_firestore_document(collection: str, document_id: str) -> str:
    """
    Check if a document exists in Firestore and show its contents.

    Args:
        collection: Collection name
        document_id: Document ID

    Returns:
        Document contents or not found message
    """
    logger.info(f"🔧 Tool called: check_firestore_document")
    logger.info(f"   Collection: {collection}")
    logger.info(f"   Document ID: {document_id}")

    service = get_firestore_native_service()
    data = service.read_from_collection(collection, document_id)

    if not data:
        result = f"❌ Document not found: {collection}/{document_id}"
        logger.warning(f"⚠️  Document not found")
        return result

    result = f"""✅ Document found: {collection}/{document_id}

Contents:
"""
    for key, value in data.items():
        result += f"   {key}: {value}\n"

    logger.info(f"✅ Tool completed successfully")
    return result


# Example usage
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTING AGENT TOOLS WITH LOGGING")
    print("=" * 80 + "\n")

    # Enable console logging to see all logs
    logging.basicConfig(level=logging.INFO)

    # Test 1: Save food preferences
    print("\n1. Testing save_patient_food_preferences...")
    print("-" * 80)
    result = save_patient_food_preferences(
        patient_id='John',
        likes='grilled chicken, steamed vegetables, brown rice',
        dislikes='spicy food, seafood',
        allergies='peanuts',
        notes='Prefers smaller, frequent meals'
    )
    print(result)

    # Test 2: Get food preferences
    print("\n2. Testing get_patient_food_preferences...")
    print("-" * 80)
    result = get_patient_food_preferences('John')
    print(result)

    # Test 3: Add care instruction
    print("\n3. Testing add_patient_care_instruction...")
    print("-" * 80)
    result = add_patient_care_instruction(
        patient_id='John',
        instruction='Ensure water intake throughout the day'
    )
    print(result)

    # Test 4: Get care instructions
    print("\n4. Testing get_patient_care_instructions...")
    print("-" * 80)
    result = get_patient_care_instructions('John')
    print(result)

    # Test 5: List collections
    print("\n5. Testing list_firestore_collections...")
    print("-" * 80)
    result = list_firestore_collections()
    print(result)

    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE - Check logs above to see Firestore operations")
    print("=" * 80)
