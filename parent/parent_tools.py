"""Tools for the Parent Agent to coordinate the workshop management system."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from team29.mock_data import (
    generate_appointments,
    generate_movement_data,
    generate_presence_data,
    generate_motion_sensor_data,
    generate_daily_behavior_data,
    generate_irregularities,
    generate_caregiver_profile,
    generate_medical_documentation
)
from team29.tools import (
    format_schedule,
    summarize_daily_data,
    check_medication_compliance,
    calculate_time_until_appointment
)


def route_to_caregiver(query: str) -> str:
    """
    Route caregiver-related queries about schedules and tasks ONLY.

    🚨 DO NOT USE for food preferences - those should be saved directly to Firestore!

    When caregiver agent is available, this will delegate to it.

    Args:
        query: The caregiver-related question or request (schedules, task lists only)

    Returns:
        Response about routing or mock response

    Note: Food preferences should use save_patient_food_preferences() instead!
    """
    return f"""[ROUTING TO CAREGIVER AGENT]
Query: {query}

Note: This will be handled by the caregiver agent once implemented by your teammate.
The caregiver agent will handle:
- Daily schedules and appointments
- Task lists and reminders
- Caregiver shift information
- Daily observations and notes

⚠️  FOOD PREFERENCES should be saved directly to Firestore, not routed here!"""


def route_to_doctor(query: str) -> str:
    """
    Route medical/doctor-related queries. When doctor agent is available, this will delegate to it.

    Args:
        query: The medical or doctor-related question or request

    Returns:
        Response about routing or mock response
    """
    return f"""[ROUTING TO DOCTOR AGENT]
Query: {query}

Note: This will be handled by the doctor agent once implemented by your teammate.
The doctor agent will handle:
- Medical documentation
- Doctor appointments and consultations
- Prescription management
- Medical history and records"""


def route_to_data_collector(query: str) -> str:
    """
    Route data collection queries. When data collection agent is available, this will delegate to it.

    Args:
        query: The data-related question or request

    Returns:
        Response about routing or mock response
    """
    return f"""[ROUTING TO DATA COLLECTION AGENT]
Query: {query}

Note: This will be handled by the daily data collection agent once implemented by your teammate.
The data agent will handle:
- Movement and activity data
- Presence and location tracking
- Motion sensor data
- Behavioral pattern analysis
- Irregularity detection"""


def get_daily_summary(date: Optional[str] = None) -> str:
    """
    Get a comprehensive daily summary combining all data sources.

    Args:
        date: The date to get summary for (default: today)

    Returns:
        Comprehensive daily summary
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Gather all data
    movement = generate_movement_data(date)
    presence = generate_presence_data(date)
    sensors = generate_motion_sensor_data(date)
    behavior = generate_daily_behavior_data(date)
    irregularities = generate_irregularities(date)

    # Create comprehensive summary
    summary = f"""📊 Daily Summary for {date}

🏃 ACTIVITY & MOVEMENT:
- Steps: {movement['total_steps']}
- Active time: {movement['active_minutes']} minutes
- Distance: {movement['distance_km']} km

🏠 PRESENCE:
- Time at home: {presence['home_hours']} hours
- Outings: {len(presence['outings'])}

🛏️ SLEEP & REST:
- Sleep duration: {behavior['sleep_hours']} hours
- Sleep quality: {behavior['sleep_quality']}

🍽️ MEALS:
- Breakfast: {'✓' if behavior['meal_times'][0]['eaten'] else '✗'}
- Lunch: {'✓' if behavior['meal_times'][1]['eaten'] else '✗'}
- Dinner: {'✓' if behavior['meal_times'][2]['eaten'] else '✗'}

💊 MEDICATION:
- Compliance: {'✓ On track' if behavior['medication_compliance'] else '⚠️ Missed dose'}

😊 MOOD & WELLBEING:
- Mood: {behavior['mood']}
- Social interactions: {behavior['social_interactions']}

🔍 MOTION SENSORS:
- Active rooms: {len(sensors['active_rooms'])}
- Overnight bathroom visits: {sensors['overnight_bathroom_visits']}
"""

    if irregularities:
        summary += "\n⚠️ IRREGULARITIES DETECTED:\n"
        for irr in irregularities:
            severity_icon = "🔴" if irr['severity'] == 'high' else "🟡" if irr['severity'] == 'medium' else "🟢"
            summary += f"{severity_icon} [{irr['severity'].upper()}] {irr['description']}\n"
    else:
        summary += "\n✅ No irregularities detected today.\n"

    return summary


def get_upcoming_appointments(days: int = 7) -> str:
    """
    Get upcoming appointments for the next N days.

    Args:
        days: Number of days to look ahead (default: 7)

    Returns:
        Formatted list of upcoming appointments
    """
    appointments = generate_appointments(days_ahead=days)
    if not appointments:
        return f"No appointments scheduled for the next {days} days."

    output = f"📅 Upcoming Appointments (Next {days} days):\n\n"
    for apt in appointments[:10]:  # Limit to 10 appointments
        time_until = calculate_time_until_appointment(apt['time'])
        output += f"• {apt['title']}\n"
        output += f"  Type: {apt['type']} | Time: {apt['time']} ({time_until})\n"
        if apt.get('notes'):
            output += f"  Notes: {apt['notes']}\n"
        output += "\n"

    return output


def check_irregularities(date: Optional[str] = None) -> str:
    """
    Check for any irregularities or concerning patterns.

    Args:
        date: The date to check (default: today)

    Returns:
        Report of any irregularities found
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    irregularities = generate_irregularities(date)

    if not irregularities:
        return f"✅ No irregularities detected for {date}. Everything appears normal."

    output = f"⚠️ Irregularities Report for {date}:\n\n"
    output += f"Total irregularities: {len(irregularities)}\n\n"

    for irr in irregularities:
        severity_icon = "🔴" if irr['severity'] == 'high' else "🟡" if irr['severity'] == 'medium' else "🟢"
        output += f"{severity_icon} [{irr['severity'].upper()}] {irr['type'].upper()}\n"
        output += f"   Time: {irr['timestamp']}\n"
        output += f"   Description: {irr['description']}\n\n"

    # Add recommendations
    high_severity = [i for i in irregularities if i['severity'] == 'high']
    if high_severity:
        output += "🚨 RECOMMENDATIONS:\n"
        output += "- Contact caregiver immediately\n"
        output += "- Review recent activity patterns\n"
        output += "- Consider scheduling a check-in call\n"

    return output


def get_medical_summary() -> str:
    """
    Get a summary of recent medical documentation and appointments.

    Returns:
        Summary of medical information
    """
    docs = generate_medical_documentation()

    output = "📋 Medical Documentation Summary:\n\n"
    output += f"Total documents: {len(docs)}\n\n"

    for doc in docs:
        output += f"• {doc['title']}\n"
        output += f"  Type: {doc['type']} | Date: {doc['date']}\n"
        output += f"  Provider: {doc['provider']}\n"

        if doc['type'] == 'prescription' and 'medications' in doc:
            output += "  Medications:\n"
            for med in doc['medications']:
                output += f"    - {med['name']}: {med['dosage']}, {med['frequency']}\n"
        elif 'summary' in doc:
            output += f"  Summary: {doc['summary']}\n"
        elif 'results' in doc:
            output += f"  Results: {doc['results']}\n"

        output += "\n"

    return output


def analyze_trends(days: int = 7) -> str:
    """
    Analyze trends over the past N days.

    Args:
        days: Number of days to analyze (default: 7)

    Returns:
        Trend analysis report
    """
    # Generate data for multiple days
    from datetime import timedelta

    base_date = datetime.now()
    daily_data = []

    for i in range(days):
        date = (base_date - timedelta(days=i)).strftime("%Y-%m-%d")
        daily_data.append({
            'date': date,
            'movement': generate_movement_data(date),
            'behavior': generate_daily_behavior_data(date),
            'irregularities': generate_irregularities(date)
        })

    # Calculate averages
    avg_steps = sum(d['movement']['total_steps'] for d in daily_data) / days
    avg_sleep = sum(d['behavior']['sleep_hours'] for d in daily_data) / days
    total_irregularities = sum(len(d['irregularities']) for d in daily_data)

    output = f"📈 {days}-Day Trend Analysis:\n\n"
    output += f"ACTIVITY:\n"
    output += f"- Average daily steps: {int(avg_steps)}\n"
    output += f"- Trend: {'↗️ Increasing' if avg_steps > 3000 else '↘️ Decreasing'}\n\n"

    output += f"SLEEP:\n"
    output += f"- Average sleep: {avg_sleep:.1f} hours\n"
    output += f"- Quality: {'Good' if avg_sleep >= 7 else 'Needs attention'}\n\n"

    output += f"IRREGULARITIES:\n"
    output += f"- Total in {days} days: {total_irregularities}\n"
    output += f"- Status: {'⚠️ Concerning' if total_irregularities > days else '✅ Normal'}\n\n"

    return output


def answer_common_question(question: str) -> str:
    """
    Answer common questions that don't require specialist agents.

    Args:
        question: The question to answer

    Returns:
        Answer to common question
    """
    # This is a catch-all for simple questions
    return f"""I can help you with:
- Daily summaries and activity reports
- Upcoming appointments and schedules
- Irregularity monitoring and alerts
- Medical documentation overview
- Trend analysis

For specific questions about:
- Caregiving tasks → I'll route to the caregiver agent
- Medical details → I'll route to the doctor agent
- Data collection → I'll route to the data collection agent

Your question: "{question}"

How can I assist you with this?"""
