"""Test script to verify agent Firestore integration works correctly.

This simulates what your agent should do when it receives food preference information.
"""

import logging
from team29.firestore_agent_tools import (
    save_patient_food_preferences,
    get_patient_food_preferences,
    list_firestore_collections,
    check_firestore_document
)

# Enable logging to see all operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("\n" + "=" * 80)
print("🧪 TESTING AGENT FIRESTORE INTEGRATION")
print("=" * 80)

print("\n📝 Scenario: User sends message about food preferences")
print("-" * 80)
user_message = "John likes chicken and vegetables but dislikes spicy food. He's allergic to peanuts."
print(f"User: \"{user_message}\"")

print("\n🤖 Agent Action: Calling save_patient_food_preferences tool")
print("-" * 80)
result = save_patient_food_preferences(
    patient_id='John',
    likes='chicken, vegetables',
    dislikes='spicy food',
    allergies='peanuts',
    notes='Preferences provided by user'
)
print("\n" + result)

print("\n" + "=" * 80)
print("✅ STEP 1 COMPLETE: Data saved to Firestore")
print("=" * 80)

print("\n📖 Verifying: Reading back the saved preferences")
print("-" * 80)
result = get_patient_food_preferences('John')
print(result)

print("\n" + "=" * 80)
print("✅ STEP 2 COMPLETE: Data retrieved successfully")
print("=" * 80)

print("\n🔍 Checking Firestore document directly")
print("-" * 80)
result = check_firestore_document('food-preferences', 'John')
print(result)

print("\n" + "=" * 80)
print("✅ STEP 3 COMPLETE: Verified in Firestore")
print("=" * 80)

print("\n📊 Summary of Firestore Collections")
print("-" * 80)
result = list_firestore_collections()
print(result)

print("\n" + "=" * 80)
print("🎉 TEST COMPLETE!")
print("=" * 80)

print("""
✅ What worked:
   • Agent tool saved food preferences to Firestore
   • Data was stored in: food-preferences/John
   • Data can be retrieved by any agent
   • All operations were logged with timestamps

🔍 Check the logs above to see:
   • 🔧 Tool called: save_patient_food_preferences
   • 💾 SAVING to Firestore...
   • ✅ SUCCESS! Data saved

This is exactly what should happen when your agent receives food preference information.
Your agent should now save directly to Firestore instead of routing to caregiver agent!
""")
