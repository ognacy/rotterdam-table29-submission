"""Real-time Firestore monitor to see when data changes.

Run this script to watch Firestore activity in real-time.
"""

import os
import time
from datetime import datetime
from google.cloud import firestore

# Connect to Firestore
project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'qwiklabs-gcp-04-b310107eab82')
db = firestore.Client(project=project_id, database='default')

print("=" * 80)
print("🔍 FIRESTORE REAL-TIME MONITOR")
print("=" * 80)
print(f"Project: {project_id}")
print(f"Database: default")
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print("\nWatching for changes... (Press Ctrl+C to stop)\n")


# Track document states
document_cache = {}


def check_collection(collection_name):
    """Check a collection for changes."""
    try:
        docs = db.collection(collection_name).stream()

        for doc in docs:
            doc_id = doc.id
            doc_data = doc.to_dict()
            cache_key = f"{collection_name}/{doc_id}"

            # Check if this is a new document or changed
            if cache_key not in document_cache:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✨ NEW DOCUMENT")
                print(f"   📂 {collection_name}/{doc_id}")
                print(f"   📝 Fields: {list(doc_data.keys())}")
                for key, value in doc_data.items():
                    value_str = str(value)
                    if len(value_str) > 100:
                        value_str = value_str[:97] + "..."
                    print(f"      {key}: {value_str}")
                print()
                document_cache[cache_key] = doc_data
            elif document_cache[cache_key] != doc_data:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 UPDATED DOCUMENT")
                print(f"   📂 {collection_name}/{doc_id}")

                # Show what changed
                for key in doc_data:
                    if key not in document_cache[cache_key] or document_cache[cache_key][key] != doc_data[key]:
                        old_value = document_cache[cache_key].get(key, '(not set)')
                        new_value = doc_data[key]
                        print(f"      {key}:")
                        print(f"         Old: {old_value}")
                        print(f"         New: {new_value}")
                print()
                document_cache[cache_key] = doc_data

    except Exception as e:
        print(f"Error checking {collection_name}: {e}")


# Get all collections
collections = [col.id for col in db.collections()]
print(f"Monitoring {len(collections)} collections:")
for col in collections:
    print(f"   • {col}")
print()

# Initial scan
print("📊 Initial scan...")
for collection_name in collections:
    check_collection(collection_name)
print("✅ Initial scan complete. Watching for changes...\n")

# Monitor loop
try:
    while True:
        for collection_name in collections:
            check_collection(collection_name)

        time.sleep(2)  # Check every 2 seconds

except KeyboardInterrupt:
    print("\n\n" + "=" * 80)
    print("🛑 Monitor stopped")
    print("=" * 80)
