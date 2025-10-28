"""Shared tools and functions for the workshop management system."""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import random


def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_schedule(appointments: List[Dict[str, Any]]) -> str:
    """Format a list of appointments into a readable schedule."""
    if not appointments:
        return "No appointments scheduled."

    schedule = "Schedule:\n"
    for apt in sorted(appointments, key=lambda x: x.get('time', '')):
        schedule += f"- {apt.get('time', 'TBD')}: {apt.get('title', 'Untitled')} ({apt.get('type', 'general')})\n"
        if apt.get('notes'):
            schedule += f"  Notes: {apt['notes']}\n"
    return schedule


def parse_caregiver_instructions(instructions: str) -> Dict[str, List[str]]:
    """Parse caregiver instructions into categories."""
    categories = {
        'morning': [],
        'afternoon': [],
        'evening': [],
        'medications': [],
        'special_notes': []
    }

    # Simple parsing logic - can be enhanced with NLP
    lines = instructions.split('\n')
    current_category = 'special_notes'

    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower_line = line.lower()
        if 'morning' in lower_line:
            current_category = 'morning'
        elif 'afternoon' in lower_line:
            current_category = 'afternoon'
        elif 'evening' in lower_line:
            current_category = 'evening'
        elif 'medication' in lower_line or 'medicine' in lower_line:
            current_category = 'medications'
        else:
            categories[current_category].append(line)

    return categories


def calculate_time_until_appointment(appointment_time: str) -> str:
    """Calculate time remaining until an appointment."""
    try:
        apt_dt = datetime.strptime(appointment_time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        delta = apt_dt - now

        if delta.total_seconds() < 0:
            return "Past appointment"

        hours = delta.total_seconds() / 3600
        if hours < 1:
            return f"{int(delta.total_seconds() / 60)} minutes"
        elif hours < 24:
            return f"{int(hours)} hours"
        else:
            return f"{int(hours / 24)} days"
    except:
        return "Unknown"


def prioritize_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Prioritize tasks based on urgency and importance."""
    priority_weights = {
        'urgent': 3,
        'high': 2,
        'medium': 1,
        'low': 0
    }

    return sorted(tasks,
                  key=lambda x: priority_weights.get(x.get('priority', 'low'), 0),
                  reverse=True)


def summarize_daily_data(data: Dict[str, Any]) -> str:
    """Summarize daily sensor and behavioral data."""
    summary = "Daily Summary:\n"

    if 'movement' in data:
        movement = data['movement']
        summary += f"- Movement: {movement.get('total_steps', 0)} steps, "
        summary += f"{movement.get('active_minutes', 0)} active minutes\n"

    if 'presence' in data:
        presence = data['presence']
        summary += f"- Presence: Home for {presence.get('home_hours', 0)} hours\n"

    if 'motion_sensors' in data:
        sensors = data['motion_sensors']
        summary += f"- Activity detected in {len(sensors.get('active_rooms', []))} rooms\n"

    if 'irregularities' in data and data['irregularities']:
        summary += f"- ⚠️ Irregularities detected: {len(data['irregularities'])} items\n"

    return summary


def check_medication_compliance(schedule: List[Dict], taken: List[Dict]) -> Dict[str, Any]:
    """Check if medications were taken as scheduled."""
    scheduled_count = len(schedule)
    taken_count = len(taken)

    compliance_rate = (taken_count / scheduled_count * 100) if scheduled_count > 0 else 0

    missed = []
    for med in schedule:
        if not any(t.get('medication_id') == med.get('id') for t in taken):
            missed.append(med.get('name', 'Unknown medication'))

    return {
        'compliance_rate': compliance_rate,
        'scheduled': scheduled_count,
        'taken': taken_count,
        'missed': missed,
        'status': 'good' if compliance_rate >= 90 else 'needs_attention'
    }
