import json
from datetime import datetime, timedelta, time as dt_time
from typing import Dict, Any, List

from google.cloud import firestore

# ---------- Helpers

def parse_iso8601(dt_str: str) -> datetime:
    """
    Parse an ISO-8601 datetime string into a naive datetime (no tz) as requested.
    Accepts forms like '2025-10-27T07:00:00' or '2025-10-27 07:00:00'.
    """
    # Try a few common formats without timezone; ignore timezone conversions per requirements.
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(dt_str, fmt)
            # If only a date was given, default to 07:00 to clearly fall in the 06:00–14:00 shift
            if fmt == "%Y-%m-%d":
                dt = datetime.combine(dt.date(), dt_time(7, 0, 0))
            return dt
        except ValueError:
            pass
    raise ValueError("current_date must be ISO-like, e.g. '2025-10-27T07:00:00'")

def shift_start_for(dt: datetime) -> datetime:
    """
    Given a naive datetime, return the datetime of the START of the shift that covers dt.
    Shifts start at 06:00, 14:00, 22:00. Times between 00:00-05:59 belong to previous day's 22:00 shift.
    """
    h = dt.hour
    if 6 <= h < 14:
        return datetime.combine(dt.date(), dt_time(6, 0, 0))
    elif 14 <= h < 22:
        return datetime.combine(dt.date(), dt_time(14, 0, 0))
    elif h >= 22:
        return datetime.combine(dt.date(), dt_time(22, 0, 0))
    else:  # 00:00-05:59 → previous day 22:00
        prev = dt.date() - timedelta(days=1)
        return datetime.combine(prev, dt_time(22, 0, 0))

def shift_number_for(dt: datetime) -> int:
    """
    Compute 1-based shift number within a non-leap-year: (day_of_year-1)*3 + shift_index (1..3).
    """
    start = shift_start_for(dt)
    day_of_year = int(start.strftime("%j"))  # 1..365
    start_hour = start.hour
    if start_hour == 6:
        index = 1
    elif start_hour == 14:
        index = 2
    else:  # 22
        index = 3
    return (day_of_year - 1) * 3 + index  # 1..1095

def previous_shift_number(n: int) -> int:
    return 1095 if n <= 1 else (n - 1)

def stringify(v: Any) -> str:
    if isinstance(v, bool):
        return "True" if v else "False"
    return "" if v is None else str(v)

def within_last_week(ts: datetime, now_ref: datetime) -> bool:
    return (now_ref - ts) <= timedelta(days=7)

def parse_ts(s: str) -> datetime:
    # Be lenient for sample/demo: accept ISO with/without seconds and 'Z'
    s = s.replace("Z", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            if fmt == "%Y-%m-%d":
                dt = datetime.combine(dt.date(), dt_time(0, 0, 0))
            return dt
        except ValueError:
            continue
    # If parsing fails, treat as very old so it gets filtered out
    return datetime(1970, 1, 1)

# ---------- Core Firestore Access

def get_collection_doc_as_string(db, collection: str, doc_id: str) -> str:
    doc_ref = db.collection(collection).document(doc_id)
    snap = doc_ref.get()
    if not snap.exists:
        return ""
    data = snap.to_dict() or {}
    # Prefer a 'value' or 'summary' field; else stringify the whole doc
    for key in ("value", "summary", "text", "status"):
        if key in data:
            return stringify(data[key])
    # Fallback: compact one-line representation
    return stringify(data)

def load_notes(db, patient_name: str, now_ref: datetime, caregiver_taking_over: str) -> Dict[str, List[Dict[str, Any]]]:
    parent_ref = db.collection("parent-notes").document(patient_name)
    caregiver_ref = db.collection("caregiver-notes").document(patient_name)

    parent_notes = []
    caregiver_notes = []

    p = parent_ref.get()
    if p.exists:
        arr = p.to_dict().get("notes", []) or p.to_dict().get("items", []) or []
        # normalize
        norm = []
        for item in arr:
            ts = parse_ts(str(item.get("timestamp", "")))
            if within_last_week(ts, now_ref):
                norm.append({
                    "timestamp": ts.isoformat(),
                    "note": item.get("note", "")
                })
        # newest first
        parent_notes = sorted(norm, key=lambda x: x["timestamp"], reverse=True)[:3]

    c = caregiver_ref.get()
    if c.exists:
        arr = c.to_dict().get("notes", []) or c.to_dict().get("items", []) or []
        norm = []
        for item in arr:
            cg = item.get("caregiver", "")
            if cg and caregiver_taking_over and cg.strip().lower() == caregiver_taking_over.strip().lower():
                continue  # exclude the incoming caregiver's own notes
            ts = parse_ts(str(item.get("timestamp", "")))
            if within_last_week(ts, now_ref):
                norm.append({
                    "timestamp": ts.isoformat(),
                    "caregiver": cg,
                    "note": item.get("note", "")
                })
        caregiver_notes = sorted(norm, key=lambda x: x["timestamp"], reverse=True)[:3]

    return {
        "parent-notes": parent_notes,
        "caregiver-notes": caregiver_notes,
    }

def load_appointments_for_day(db, patient_name: str, on_date: datetime) -> List[Dict[str, Any]]:
    ref = db.collection("appointments").document(patient_name)
    snap = ref.get()
    if not snap.exists:
        return []
    items = snap.to_dict().get("appointments", []) or snap.to_dict().get("items", []) or []
    result = []
    for appt in items:
        ts = parse_ts(str(appt.get("appointment_date", "")))
        if ts.date() == on_date.date():
            result.append({
                "appointment_date": ts.isoformat(),
                "type": appt.get("type", ""),
                "details": appt.get("details", ""),
                "where": appt.get("where", "")
            })
    # Sort by time in day
    result.sort(key=lambda x: x["appointment_date"])
    return result

# ---------- HTTP Cloud Functions

def get_shift_start_summary(request):
    """
    HTTP POST with JSON body:
    {
      "patient_name": "John",
      "current_date": "2025-10-27T07:00:00",
      "caregiver_taking_over": "Alice"
    }
    """
    if request.method == "OPTIONS":
        # CORS preflight
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

    try:
        body = request.get_json(silent=True) or {}
        patient_name = body.get("patient_name") or body.get("patient") or ""
        current_date_str = body.get("current_date") or ""
        caregiver_taking_over = body.get("caregiver_taking_over") or ""

        if not patient_name or not current_date_str:
            return (json.dumps({"error": "patient_name and current_date are required"}), 400, headers)

        current_dt = parse_iso8601(current_date_str)
        # Compute current and previous shifts
        current_shift = shift_number_for(current_dt)
        prev_shift = previous_shift_number(current_shift)

        prev_doc_id = f"{patient_name}-shift-{prev_shift}"

        db = firestore.Client()

        # Pull collections for previous shift
        collections = [
            "caregiver_in_charge",
            "anything_unusual",
            "shift_summary",
            "meds",
            "food",
            "hr",
            "movement",
        ]
        fetched = {col: get_collection_doc_as_string(db, col, prev_doc_id) for col in collections}

        # Caregiver notes and parent notes (last 3, within 1 week; exclude incoming caregiver from caregiver-notes)
        notes = load_notes(db, patient_name, now_ref=current_dt, caregiver_taking_over=caregiver_taking_over)

        # Appointments scheduled "today" (same calendar date as current_date)
        todays_appts = load_appointments_for_day(db, patient_name, current_dt)

        # Build the output structure
        result = {
            "shift_start_summary": {
                "appointments_scheduled_today": todays_appts,
                "caregiver-notes": notes["caregiver-notes"],
                "parent-notes": notes["parent-notes"],
                "previous_shift": {
                    "caregiver_in_charge": fetched.get("caregiver_in_charge", ""),
                    "caregiver_in_charge_pronouns": "",  # will try to pick a pronouns field if present below
                    "anything_unusual": stringify(fetched.get("anything_unusual", "")),
                    "shift_summary": stringify(fetched.get("shift_summary", "")),
                    "meds": stringify(fetched.get("meds", "")),
                    "food": stringify(fetched.get("food", "")),
                    "hr": stringify(fetched.get("hr", "")),
                    "movement": stringify(fetched.get("movement", "")),
                },
                "meta": {
                    "patient_name": patient_name,
                    "current_date": current_dt.isoformat(),
                    "current_shift_number": current_shift,
                    "previous_shift_number": prev_shift,
                }
            }
        }

        # Try to fetch pronouns field specifically if it exists
        # (If caregiver_in_charge doc was a dict string, we can't see inside; try a second read as dict)
        cg_snap = firestore.Client().collection("caregiver_in_charge").document(prev_doc_id).get()
        if cg_snap.exists and isinstance(cg_snap.to_dict(), dict):
            pron = cg_snap.to_dict().get("caregiver_in_charge_pronouns")
            if pron:
                result["shift_start_summary"]["previous_shift"]["caregiver_in_charge_pronouns"] = pron

        return (json.dumps(result), 200, headers)

    except Exception as e:
        return (json.dumps({"error": str(e)}), 500, headers)

# ---------- Sample data creator (HTTP)

def create_sample_data_http(request):
    """
    Seed Firestore with creative demo data for patient 'John' around ±2 days of 2025-10-27
    and caregiver 'Alice'. This creates:
      - previous shifts' docs for all required collections
      - parent-notes/John
      - caregiver-notes/John
      - appointments/John
    """
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}

    try:
        db = firestore.Client()

        patient_name = "John"
        caregiver_name = "Alice"
        # Anchor date: 2025-10-27 07:00 (falls in 06:00-14:00 shift)
        anchor = datetime(2025, 10, 27, 7, 0, 0)

        # Create a few timestamped notes around ±2 days
        times = [
            anchor - timedelta(days=2, hours=3),
            anchor - timedelta(days=1, hours=1),
            anchor - timedelta(hours=5),
            anchor - timedelta(hours=1),
            anchor,
            anchor + timedelta(hours=4),
            anchor + timedelta(days=1, hours=2),
            anchor + timedelta(days=2, hours=1),
        ]

        # ---- Shifts for previous days (populate doc per collection for previous shift)
        # We'll use the immediately previous shift to anchor output to something meaningful
        prev_shift_num = previous_shift_number(shift_number_for(anchor))
        prev_doc_id = f"{patient_name}-shift-{prev_shift_num}"

        db.collection("caregiver_in_charge").document(prev_doc_id).set({
            "value": caregiver_name,
            "caregiver_in_charge_pronouns": "she/her",
        })
        db.collection("anything_unusual").document(prev_doc_id).set({
            "value": False,
            "details": "Slept through the night without issues"
        })
        db.collection("shift_summary").document(prev_doc_id).set({
            "summary": "Good night's sleep; responsive in the morning; enjoyed reading time."
        })
        db.collection("meds").document(prev_doc_id).set({
            "value": "All taken as scheduled; Vitamin D at 07:30."
        })
        db.collection("food").document(prev_doc_id).set({
            "value": "Breakfast: oatmeal + berries; Snack: yogurt."
        })
        db.collection("hr").document(prev_doc_id).set({
            "value": "normal (resting 62–68 bpm)"
        })
        db.collection("movement").document(prev_doc_id).set({
            "value": "average movement; short walk after breakfast."
        })

        # ---- Parent notes
        parent_notes = [
            {"timestamp": (times[1]).isoformat(), "note": "Asked about favorite songs; perked up hearing old playlist."},
            {"timestamp": (times[3]).isoformat(), "note": "Please encourage water intake this afternoon."},
            {"timestamp": (times[4]).isoformat(), "note": "We’ll visit tomorrow after lunch."},
            {"timestamp": (times[6]).isoformat(), "note": "Brought a new sweater; it's in the top drawer."},
        ]
        db.collection("parent-notes").document(patient_name).set({"notes": parent_notes})

        # ---- Caregiver notes (mix of Alice + others; we will filter Alice)
        caregiver_notes = [
            {"timestamp": (times[0]).isoformat(), "caregiver": "Bob", "note": "Light stretching helped ease stiffness."},
            {"timestamp": (times[2]).isoformat(), "caregiver": "Alice", "note": "Refused tea; preferred warm water."},
            {"timestamp": (times[3]).isoformat(), "caregiver": "Carol", "note": "Enjoyed a short story; calm mood."},
            {"timestamp": (times[5]).isoformat(), "caregiver": "Alice", "note": "Walked 200m around the garden."},
            {"timestamp": (times[7]).isoformat(), "caregiver": "Derek", "note": "Prefers the blue slippers."},
        ]
        db.collection("caregiver-notes").document(patient_name).set({"notes": caregiver_notes})

        # ---- Appointments (some today; some other days)
        appts = [
            {
                "appointment_date": datetime(2025, 10, 27, 11, 0, 0).isoformat(),
                "type": "doctor consult",
                "details": "Dietician check-in",
                "where": "Clinic A, Main St 123"
            },
            {
                "appointment_date": datetime(2025, 10, 27, 16, 30, 0).isoformat(),
                "type": "physio",
                "details": "Gait assessment",
                "where": "Physio Center, Park Ave 5"
            },
            {
                "appointment_date": datetime(2025, 10, 28, 9, 0, 0).isoformat(),
                "type": "lab",
                "details": "Routine bloodwork",
                "where": "Lab B, Riverside 9"
            }
        ]
        db.collection("appointments").document(patient_name).set({"appointments": appts})

        return (json.dumps({
            "status": "ok",
            "seeded_prev_shift_doc_id": prev_doc_id,
            "patient_name": patient_name,
            "caregiver_name": caregiver_name
        }), 200, headers)

    except Exception as e:
        return (json.dumps({"error": str(e)}), 500, headers)

