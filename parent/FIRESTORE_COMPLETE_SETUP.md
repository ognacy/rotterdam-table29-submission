# ✅ Firestore Native - Complete Setup with Logging

## What You Have Now

✅ **Firestore Native Service** (`firestore_native_service.py`)
- Low-level Firestore operations with detailed logging
- Every read/write operation is logged with timestamps

✅ **Agent Tools** (`firestore_agent_tools.py`)
- High-level tools your agents can use
- All operations logged for debugging

✅ **Real-time Monitor** (`monitor_firestore.py`)
- Watch Firestore changes in real-time
- See new documents and updates as they happen

✅ **Documentation** (`FIRESTORE_LOGGING_GUIDE.md`)
- Complete guide on using the logging system

## Your Firestore Setup

**Database**: `default` (Firestore Native Mode)
**Project**: `qwiklabs-gcp-04-b310107eab82`
**Location**: `europe-west1`

### Collections in Your Database

| Collection | What It Stores |
|------------|----------------|
| `food-preferences` | Detailed dietary preferences (likes, dislikes, allergies) |
| `food` | Daily food intake |
| `care-instructions` | Long-term care instructions |
| `caregiver-notes` | Notes from caregivers |
| `parent-notes` | Notes from family |
| `appointments` | Medical appointments |
| `hr` | Heart rate data |
| `movement` | Activity data |
| `meds` | Medication tracking |
| `anything_unusual` | Irregularities |
| `caregiver_in_charge` | Current caregiver |
| `shift_summary` | Shift summaries |

## How to Track Where Data is Saved

### Option 1: Run the Monitor (Recommended)

Open a terminal and run:
```bash
python team29/monitor_firestore.py
```

This will show you:
- All existing documents
- New documents as they're created
- Updates to existing documents
- Which collection and document ID

**Example output:**
```
[09:04:14] ✨ NEW DOCUMENT
   📂 food-preferences/John
   📝 Fields: ['likes', 'dislikes', 'allergies', 'notes', 'type']
      likes: ['chicken', 'vegetables']
      dislikes: ['spicy food']
      allergies: ['peanuts']
```

### Option 2: Enable Logging in Your Agent

Add to the top of `agent.py`:

```python
import logging

# Enable detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Then when your agent saves data, you'll see:
```
2025-10-28 09:04:14 - FirestoreNativeService - INFO - 💾 SAVING to Firestore...
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Collection: food-preferences
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Document ID: John
2025-10-28 09:04:14 - FirestoreNativeService - INFO - ✅ SUCCESS! Data saved
```

### Option 3: Check After Creating Message

After your agent processes a message, run:

```bash
python -c "
from team29.firestore_native_service import get_firestore_native_service

service = get_firestore_native_service()

# Check food preferences
prefs = service.get_food_preferences('John')
print('Food Preferences:', prefs)

# Check care instructions
instructions = service.get_care_instructions('John')
print('Care Instructions:', instructions)

# List all collections
collections = service.list_all_collections()
print('Collections:', collections)
"
```

## Integration with Your Agent

Add these tools to your `agent.py`:

```python
from google.adk.tools.function_tool import FunctionTool
from team29.firestore_agent_tools import (
    save_patient_food_preferences,
    get_patient_food_preferences,
    add_patient_care_instruction,
    get_patient_care_instructions,
    save_patient_food_intake,
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='parent_assistant',
    tools=[
        # Your existing tools...

        # Firestore tools (with automatic logging)
        FunctionTool(func=save_patient_food_preferences),
        FunctionTool(func=get_patient_food_preferences),
        FunctionTool(func=add_patient_care_instruction),
        FunctionTool(func=get_patient_care_instructions),
        FunctionTool(func=save_patient_food_intake),
    ],

    instruction="""...

    When the user provides information about food preferences, use save_patient_food_preferences().
    When the user asks about dietary information, use get_patient_food_preferences().
    When adding care instructions, use add_patient_care_instruction().

    All data will be automatically saved to Firestore with full logging.
    """
)
```

## Test the Complete Flow

1. **Start the monitor:**
   ```bash
   python team29/monitor_firestore.py
   ```

2. **In another terminal, test the tools:**
   ```bash
   python -m team29.firestore_agent_tools
   ```

3. **Watch the monitor** - You'll see:
   - New documents being created
   - Exact collection/document locations
   - All the data being saved

4. **Check in Firestore Console:**
   ```
   https://console.firebase.google.com/project/qwiklabs-gcp-04-b310107eab82/firestore/databases/default/data
   ```

## Example: Saving Food Preferences

### User Message to Agent:
```
"John likes grilled chicken and vegetables but dislikes spicy food. He's allergic to peanuts."
```

### Agent Uses Tool:
```python
save_patient_food_preferences(
    patient_id='John',
    likes='grilled chicken, vegetables',
    dislikes='spicy food',
    allergies='peanuts'
)
```

### What You See in Logs:
```
2025-10-28 09:04:14 - FirestoreAgentTools - INFO - 🔧 Tool called: save_patient_food_preferences
2025-10-28 09:04:14 - FirestoreAgentTools - INFO -    Patient ID: John
2025-10-28 09:04:14 - FirestoreAgentTools - INFO -    Likes: grilled chicken, vegetables
2025-10-28 09:04:14 - FirestoreAgentTools - INFO -    Dislikes: spicy food
2025-10-28 09:04:14 - FirestoreAgentTools - INFO -    Allergies: peanuts
2025-10-28 09:04:14 - FirestoreNativeService - INFO - 🔌 Connecting to Firestore Native...
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Project: qwiklabs-gcp-04-b310107eab82
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Database: default
2025-10-28 09:04:14 - FirestoreNativeService - INFO - ✅ Connected to Firestore Native successfully!
2025-10-28 09:04:14 - FirestoreNativeService - INFO - 💾 SAVING to Firestore...
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Collection: food-preferences
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Document ID: John
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Data: {'likes': ['grilled chicken', 'vegetables'], 'dislikes': ['spicy food'], 'allergies': ['peanuts'], 'type': 'dietary_preferences'}
2025-10-28 09:04:14 - FirestoreNativeService - INFO - ✅ SUCCESS! Data saved to: food-preferences/John
2025-10-28 09:04:14 - FirestoreNativeService - INFO -    Firestore path: projects/qwiklabs-gcp-04-b310107eab82/databases/default/documents/food-preferences/John
```

### What You See in Monitor:
```
[09:04:14] ✨ NEW DOCUMENT
   📂 food-preferences/John
   📝 Fields: ['likes', 'dislikes', 'allergies', 'type']
      likes: ['grilled chicken', 'vegetables']
      dislikes: ['spicy food']
      allergies: ['peanuts']
      type: dietary_preferences
```

### What You See in Firestore Console:
```
Collection: food-preferences
Document ID: John
Data: {
  likes: ['grilled chicken', 'vegetables'],
  dislikes: ['spicy food'],
  allergies: ['peanuts'],
  type: 'dietary_preferences'
}
```

## Debugging: If Data Isn't Saving

Run this checklist:

### 1. Is the agent calling the tool?
**Check logs for:**
```
🔧 Tool called: save_patient_food_preferences
```

**If NOT present:**
- Tool not added to agent's tools list
- Agent instruction not telling it to use the tool
- Agent deciding not to use the tool

### 2. Is the save succeeding?
**Check logs for:**
```
✅ SUCCESS! Data saved to: food-preferences/John
```

**If you see ❌ ERROR:**
- Read the error message
- Check authentication
- Verify Firestore API is enabled

### 3. Are you checking the right database?
**Logs should show:**
```
Database: default  ← Correct (Firestore Native)
```

**NOT:**
```
Database: (default)  ← Wrong (Datastore Mode)
```

### 4. Run diagnostic:
```bash
python -c "
from team29.firestore_native_service import get_firestore_native_service
service = get_firestore_native_service()
service.list_all_collections()
"
```

This will show all collections and confirm connection works.

## Files Reference

| File | Purpose |
|------|---------|
| `firestore_native_service.py` | Low-level Firestore operations with logging |
| `firestore_agent_tools.py` | Agent-friendly tools with logging |
| `monitor_firestore.py` | Real-time Firestore activity monitor |
| `FIRESTORE_LOGGING_GUIDE.md` | Complete logging documentation |
| `FIRESTORE_COMPLETE_SETUP.md` | This file |

## Quick Commands

```bash
# Test the tools with logging
python -m team29.firestore_agent_tools

# Monitor Firestore in real-time
python team29/monitor_firestore.py

# Check what's in Firestore
python -c "from team29.firestore_native_service import get_firestore_native_service; get_firestore_native_service().list_all_collections()"

# Get food preferences
python -c "from team29.firestore_agent_tools import get_patient_food_preferences; print(get_patient_food_preferences('John'))"
```

## Summary

✅ Firestore Native (`default` database) is properly configured
✅ All operations are logged with timestamps and details
✅ You can monitor changes in real-time
✅ Tools are ready to integrate with your agent
✅ Every save shows: where, when, what data

**No more guessing where data goes - you'll see everything! 🎉**
