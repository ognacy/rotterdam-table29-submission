"""Firestore Native Service with detailed logging.

This service connects to the 'default' Firestore Native database
and logs all read/write operations for debugging.
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from google.cloud import firestore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('FirestoreNativeService')


class FirestoreNativeService:
    """Service for Firestore Native database operations with logging."""

    def __init__(self, project_id: Optional[str] = None, database: str = 'default'):
        """Initialize Firestore Native client."""
        if project_id is None:
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'qwiklabs-gcp-04-b310107eab82')

        logger.info(f"🔌 Connecting to Firestore Native...")
        logger.info(f"   Project: {project_id}")
        logger.info(f"   Database: {database}")

        self.db = firestore.Client(project=project_id, database=database)
        self.project_id = project_id
        self.database = database

        logger.info(f"✅ Connected to Firestore Native successfully!")

    # ========== FOOD PREFERENCES ==========

    def save_food_preferences(self, patient_id: str, preferences: Dict[str, Any]) -> str:
        """
        Save food preferences for a patient.

        Args:
            patient_id: Patient identifier (e.g., 'John')
            preferences: Dict with keys like 'likes', 'dislikes', 'allergies', 'notes'

        Returns:
            Document ID
        """
        collection = 'food-preferences'
        doc_id = patient_id

        logger.info(f"💾 SAVING to Firestore...")
        logger.info(f"   Collection: {collection}")
        logger.info(f"   Document ID: {doc_id}")
        logger.info(f"   Data: {preferences}")

        try:
            doc_ref = self.db.collection(collection).document(doc_id)
            doc_ref.set(preferences, merge=True)

            logger.info(f"✅ SUCCESS! Data saved to: {collection}/{doc_id}")
            logger.info(f"   Firestore path: projects/{self.project_id}/databases/{self.database}/documents/{collection}/{doc_id}")

            return doc_id

        except Exception as e:
            logger.error(f"❌ ERROR saving to Firestore: {e}")
            raise

    def get_food_preferences(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get food preferences for a patient."""
        collection = 'food-preferences'
        doc_id = patient_id

        logger.info(f"📖 READING from Firestore...")
        logger.info(f"   Collection: {collection}")
        logger.info(f"   Document ID: {doc_id}")

        try:
            doc_ref = self.db.collection(collection).document(doc_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                logger.info(f"✅ SUCCESS! Found document with {len(data)} fields")
                logger.info(f"   Data: {data}")
                return data
            else:
                logger.warning(f"⚠️  Document not found: {collection}/{doc_id}")
                return None

        except Exception as e:
            logger.error(f"❌ ERROR reading from Firestore: {e}")
            raise

    # ========== CARE INSTRUCTIONS ==========

    def add_care_instruction(self, patient_id: str, instruction: str) -> None:
        """Add a care instruction for a patient."""
        collection = 'care-instructions'
        doc_id = patient_id

        logger.info(f"💾 ADDING instruction to Firestore...")
        logger.info(f"   Collection: {collection}")
        logger.info(f"   Document ID: {doc_id}")
        logger.info(f"   New instruction: {instruction}")

        try:
            doc_ref = self.db.collection(collection).document(doc_id)

            # Get existing instructions
            doc = doc_ref.get()
            if doc.exists:
                current_instructions = doc.to_dict().get('instructions', [])
                logger.info(f"   Found {len(current_instructions)} existing instructions")
            else:
                current_instructions = []
                logger.info(f"   No existing instructions, creating new document")

            # Add new instruction
            current_instructions.append(instruction)

            # Save back
            doc_ref.set({'instructions': current_instructions}, merge=True)

            logger.info(f"✅ SUCCESS! Instruction added to: {collection}/{doc_id}")
            logger.info(f"   Total instructions now: {len(current_instructions)}")

        except Exception as e:
            logger.error(f"❌ ERROR adding instruction: {e}")
            raise

    def get_care_instructions(self, patient_id: str) -> List[str]:
        """Get all care instructions for a patient."""
        collection = 'care-instructions'
        doc_id = patient_id

        logger.info(f"📖 READING instructions from Firestore...")
        logger.info(f"   Collection: {collection}")
        logger.info(f"   Document ID: {doc_id}")

        try:
            doc_ref = self.db.collection(collection).document(doc_id)
            doc = doc_ref.get()

            if doc.exists:
                instructions = doc.to_dict().get('instructions', [])
                logger.info(f"✅ SUCCESS! Found {len(instructions)} instructions")
                return instructions
            else:
                logger.warning(f"⚠️  No instructions found for: {patient_id}")
                return []

        except Exception as e:
            logger.error(f"❌ ERROR reading instructions: {e}")
            raise

    # ========== FOOD INTAKE (Daily) ==========

    def save_food_intake(self, patient_id: str, shift_id: str, intake: str) -> str:
        """Save daily food intake."""
        collection = 'food'
        doc_id = f"{patient_id}-{shift_id}"

        logger.info(f"💾 SAVING food intake to Firestore...")
        logger.info(f"   Collection: {collection}")
        logger.info(f"   Document ID: {doc_id}")
        logger.info(f"   Intake: {intake}")

        try:
            doc_ref = self.db.collection(collection).document(doc_id)
            doc_ref.set({'value': intake, 'timestamp': datetime.utcnow()}, merge=True)

            logger.info(f"✅ SUCCESS! Food intake saved to: {collection}/{doc_id}")

            return doc_id

        except Exception as e:
            logger.error(f"❌ ERROR saving food intake: {e}")
            raise

    # ========== GENERIC OPERATIONS ==========

    def save_to_collection(self, collection: str, doc_id: str, data: Dict[str, Any]) -> str:
        """Generic save operation with logging."""
        logger.info(f"💾 SAVING to Firestore...")
        logger.info(f"   Collection: {collection}")
        logger.info(f"   Document ID: {doc_id}")
        logger.info(f"   Data keys: {list(data.keys())}")

        try:
            doc_ref = self.db.collection(collection).document(doc_id)
            doc_ref.set(data, merge=True)

            logger.info(f"✅ SUCCESS! Data saved to: {collection}/{doc_id}")
            logger.info(f"   Full path: projects/{self.project_id}/databases/{self.database}/documents/{collection}/{doc_id}")

            return doc_id

        except Exception as e:
            logger.error(f"❌ ERROR saving to Firestore: {e}")
            logger.error(f"   Collection: {collection}")
            logger.error(f"   Document ID: {doc_id}")
            raise

    def read_from_collection(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Generic read operation with logging."""
        logger.info(f"📖 READING from Firestore...")
        logger.info(f"   Collection: {collection}")
        logger.info(f"   Document ID: {doc_id}")

        try:
            doc_ref = self.db.collection(collection).document(doc_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                logger.info(f"✅ SUCCESS! Document found with {len(data)} fields")
                return data
            else:
                logger.warning(f"⚠️  Document not found: {collection}/{doc_id}")
                return None

        except Exception as e:
            logger.error(f"❌ ERROR reading from Firestore: {e}")
            raise

    def list_all_collections(self) -> List[str]:
        """List all collections in the database."""
        logger.info(f"📂 LISTING all collections...")

        try:
            collections = [col.id for col in self.db.collections()]
            logger.info(f"✅ Found {len(collections)} collections:")
            for col in collections:
                logger.info(f"   - {col}")
            return collections

        except Exception as e:
            logger.error(f"❌ ERROR listing collections: {e}")
            raise

    def list_documents_in_collection(self, collection: str, limit: int = 10) -> List[str]:
        """List document IDs in a collection."""
        logger.info(f"📂 LISTING documents in collection: {collection}")

        try:
            docs = self.db.collection(collection).limit(limit).stream()
            doc_ids = [doc.id for doc in docs]

            logger.info(f"✅ Found {len(doc_ids)} documents:")
            for doc_id in doc_ids:
                logger.info(f"   - {doc_id}")

            return doc_ids

        except Exception as e:
            logger.error(f"❌ ERROR listing documents: {e}")
            raise


# Singleton instance
_firestore_native_service = None


def get_firestore_native_service() -> FirestoreNativeService:
    """Get or create singleton Firestore Native service instance."""
    global _firestore_native_service
    if _firestore_native_service is None:
        logger.info("🔧 Creating new FirestoreNativeService instance...")
        _firestore_native_service = FirestoreNativeService()
    return _firestore_native_service


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("FIRESTORE NATIVE SERVICE TEST")
    print("=" * 80 + "\n")

    # Initialize service
    service = get_firestore_native_service()

    # Test 1: List all collections
    print("\nTest 1: List all collections")
    print("-" * 80)
    collections = service.list_all_collections()

    # Test 2: Save food preferences
    print("\nTest 2: Save food preferences")
    print("-" * 80)
    preferences = {
        'likes': ['grilled chicken', 'vegetables', 'rice'],
        'dislikes': ['spicy food', 'seafood'],
        'allergies': ['peanuts'],
        'notes': 'Prefers smaller meals'
    }
    service.save_food_preferences('John', preferences)

    # Test 3: Read food preferences
    print("\nTest 3: Read food preferences")
    print("-" * 80)
    retrieved = service.get_food_preferences('John')
    print(f"Retrieved data: {retrieved}")

    # Test 4: List documents in food-preferences collection
    print("\nTest 4: List documents in food-preferences")
    print("-" * 80)
    service.list_documents_in_collection('food-preferences')

    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
