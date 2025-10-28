"""Mock data generators for testing the workshop management system."""

from datetime import datetime, timedelta
import random
from typing import Dict, List, Any, Optional


def generate_appointments(days_ahead: int = 7) -> List[Dict[str, Any]]:
    """Generate mock appointments for the next N days."""
    appointments = []
    appointment_types = ['doctor', 'therapy', 'social', 'exercise', 'medication_review']
    titles = {
        'doctor': ['Dr. Smith - Check-up', 'Dr. Johnson - Follow-up', 'Specialist Consultation'],
        'therapy': ['Physical Therapy', 'Occupational Therapy', 'Speech Therapy'],
        'social': ['Community Center Visit', 'Family Gathering', 'Book Club'],
        'exercise': ['Water Aerobics', 'Walking Group', 'Gentle Yoga'],
        'medication_review': ['Pharmacy Consultation', 'Medication Adjustment']
    }

    base_time = datetime.now()
    for day in range(days_ahead):
        num_appointments = random.randint(0, 3)
        for _ in range(num_appointments):
            apt_type = random.choice(appointment_types)
            apt_time = base_time + timedelta(days=day, hours=random.randint(8, 18))

            appointments.append({
                'id': f'apt_{len(appointments) + 1}',
                'title': random.choice(titles[apt_type]),
                'type': apt_type,
                'time': apt_time.strftime("%Y-%m-%d %H:%M:%S"),
                'duration_minutes': random.choice([30, 45, 60]),
                'notes': f'Remember to bring previous records.' if apt_type == 'doctor' else ''
            })

    return appointments


def generate_movement_data(date: Optional[str] = None) -> Dict[str, Any]:
    """Generate mock movement and activity data."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    return {
        'date': date,
        'total_steps': random.randint(1000, 8000),
        'active_minutes': random.randint(30, 180),
        'sedentary_minutes': random.randint(300, 600),
        'distance_km': round(random.uniform(0.5, 5.0), 2),
        'calories_burned': random.randint(200, 800),
        'hourly_activity': [random.randint(0, 500) for _ in range(24)]
    }


def generate_presence_data(date: Optional[str] = None) -> Dict[str, Any]:
    """Generate mock presence and location data."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    return {
        'date': date,
        'home_hours': round(random.uniform(18, 24), 1),
        'away_hours': round(random.uniform(0, 6), 1),
        'outings': [
            {
                'time': f'{h:02d}:00',
                'duration_minutes': random.randint(30, 180),
                'location': random.choice(['grocery store', 'park', 'community center', 'unknown'])
            }
            for h in random.sample(range(8, 18), random.randint(0, 2))
        ]
    }


def generate_motion_sensor_data(date: Optional[str] = None) -> Dict[str, Any]:
    """Generate mock motion sensor data from various rooms."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    rooms = ['bedroom', 'bathroom', 'kitchen', 'living_room', 'hallway']
    active_rooms = random.sample(rooms, random.randint(3, 5))

    return {
        'date': date,
        'active_rooms': active_rooms,
        'activity_by_room': {
            room: {
                'triggers': random.randint(5, 50),
                'last_activity': f'{random.randint(0, 23):02d}:{random.randint(0, 59):02d}',
                'total_minutes': random.randint(30, 300)
            }
            for room in active_rooms
        },
        'overnight_bathroom_visits': random.randint(0, 4),
        'unusual_patterns': random.choice([True, False])
    }


def generate_daily_behavior_data(date: Optional[str] = None) -> Dict[str, Any]:
    """Generate mock behavioral data for the day."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    return {
        'date': date,
        'sleep_hours': round(random.uniform(5, 9), 1),
        'sleep_quality': random.choice(['good', 'fair', 'poor']),
        'meal_times': [
            {'meal': 'breakfast', 'time': '08:30', 'eaten': random.choice([True, False])},
            {'meal': 'lunch', 'time': '12:30', 'eaten': random.choice([True, False])},
            {'meal': 'dinner', 'time': '18:00', 'eaten': random.choice([True, False])}
        ],
        'mood': random.choice(['happy', 'content', 'neutral', 'anxious', 'sad']),
        'social_interactions': random.randint(0, 5),
        'medication_compliance': random.choice([True, True, True, False])  # 75% compliant
    }


def generate_irregularities(date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Generate mock irregularity alerts."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    possible_irregularities = [
        {'type': 'movement', 'severity': 'medium', 'description': 'Significantly lower activity than usual'},
        {'type': 'presence', 'severity': 'high', 'description': 'Extended time away from home without notice'},
        {'type': 'sleep', 'severity': 'low', 'description': 'Slightly different sleep pattern'},
        {'type': 'medication', 'severity': 'high', 'description': 'Missed medication dose'},
        {'type': 'bathroom', 'severity': 'medium', 'description': 'Unusual number of overnight bathroom visits'},
        {'type': 'meals', 'severity': 'medium', 'description': 'Skipped multiple meals'},
        {'type': 'social', 'severity': 'low', 'description': 'No social interactions today'}
    ]

    # Return 0-2 irregularities
    num_irregularities = random.randint(0, 2)
    irregularities = random.sample(possible_irregularities, num_irregularities)

    for irr in irregularities:
        irr['date'] = date
        irr['timestamp'] = f'{random.randint(0, 23):02d}:{random.randint(0, 59):02d}'

    return irregularities


def generate_caregiver_profile() -> Dict[str, Any]:
    """Generate a mock caregiver profile."""
    return {
        'name': random.choice(['Alice Johnson', 'Bob Smith', 'Carol Martinez', 'David Lee']),
        'role': random.choice(['primary_caregiver', 'family_member', 'professional_caregiver']),
        'contact': {
            'phone': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'email': 'caregiver@example.com'
        },
        'preferences': {
            'notification_frequency': random.choice(['immediate', 'daily_digest', 'urgent_only']),
            'preferred_contact_method': random.choice(['phone', 'email', 'app']),
            'language': 'en'
        },
        'schedule': {
            'availability': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'preferred_times': ['09:00-12:00', '14:00-17:00']
        }
    }


def generate_medical_documentation() -> List[Dict[str, Any]]:
    """Generate mock medical documentation."""
    return [
        {
            'id': 'doc_1',
            'type': 'prescription',
            'date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            'provider': 'Dr. Smith',
            'title': 'Medication Prescription',
            'medications': [
                {'name': 'Lisinopril', 'dosage': '10mg', 'frequency': 'Once daily'},
                {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily'}
            ]
        },
        {
            'id': 'doc_2',
            'type': 'lab_results',
            'date': (datetime.now() - timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d"),
            'provider': 'City Lab',
            'title': 'Blood Work Results',
            'results': 'All values within normal range'
        },
        {
            'id': 'doc_3',
            'type': 'visit_summary',
            'date': (datetime.now() - timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
            'provider': 'Dr. Johnson',
            'title': 'Annual Physical Exam',
            'summary': 'Patient in good health, continue current medications'
        }
    ]
