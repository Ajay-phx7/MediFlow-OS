"""
Training data generation and management for surge prediction model
Provides historical patient data for model training
"""

from datetime import datetime, timedelta
from typing import List, Dict
import random


def generate_historical_data(days: int = 365) -> List[Dict]:
    """
    Generate synthetic historical patient data for training
    
    Args:
        days: Number of days of historical data to generate
        
    Returns:
        List of dicts with 'date' and 'patient_count' keys
    """
    data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        current_date = base_date + timedelta(days=i)
        
        # Base patient count
        base_count = 100
        
        # Weekly pattern (higher on weekdays, lower on weekends)
        day_of_week = current_date.weekday()
        if day_of_week >= 5:  # Weekend
            weekly_factor = 0.7
        else:  # Weekday
            weekly_factor = 1.0 + (day_of_week * 0.05)
        
        # Monthly pattern (higher at month start/end)
        day_of_month = current_date.day
        if day_of_month <= 5 or day_of_month >= 25:
            monthly_factor = 1.2
        else:
            monthly_factor = 1.0
        
        # Seasonal pattern (higher in winter months)
        month = current_date.month
        if month in [12, 1, 2]:  # Winter
            seasonal_factor = 1.3
        elif month in [6, 7, 8]:  # Summer
            seasonal_factor = 0.9
        else:  # Spring/Fall
            seasonal_factor = 1.0
        
        # Random variation
        random_factor = random.uniform(0.85, 1.15)
        
        # Calculate final count
        patient_count = int(
            base_count * weekly_factor * monthly_factor * 
            seasonal_factor * random_factor
        )
        
        # Add occasional surge events
        if random.random() < 0.05:  # 5% chance of surge
            patient_count = int(patient_count * random.uniform(1.4, 1.8))
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'patient_count': patient_count
        })
    
    return data


def get_recent_data(days: int = 30) -> List[Dict]:
    """
    Get recent historical data for quick training
    
    Args:
        days: Number of recent days to retrieve
        
    Returns:
        List of recent patient data
    """
    return generate_historical_data(days)


def get_training_data() -> List[Dict]:
    """
    Get full training dataset (1 year of data)
    
    Returns:
        Full historical dataset for training
    """
    return generate_historical_data(365)


def add_custom_events(data: List[Dict], events: List[Dict]) -> List[Dict]:
    """
    Add custom surge events to historical data
    
    Args:
        data: Existing historical data
        events: List of events with 'date' and 'surge_multiplier' keys
        
    Returns:
        Modified data with custom events
    """
    event_dict = {event['date']: event['surge_multiplier'] for event in events}
    
    modified_data = []
    for record in data:
        if record['date'] in event_dict:
            multiplier = event_dict[record['date']]
            modified_record = record.copy()
            modified_record['patient_count'] = int(record['patient_count'] * multiplier)
            modified_data.append(modified_record)
        else:
            modified_data.append(record)
    
    return modified_data


# Sample custom events (holidays, epidemics, etc.)
CUSTOM_EVENTS = [
    {'date': '2025-12-25', 'surge_multiplier': 0.5},  # Christmas - lower
    {'date': '2026-01-01', 'surge_multiplier': 0.6},  # New Year - lower
    {'date': '2026-01-15', 'surge_multiplier': 1.8},  # Flu season peak
    {'date': '2026-02-14', 'surge_multiplier': 1.3},  # Valentine's Day surge
]


def get_training_data_with_events() -> List[Dict]:
    """
    Get training data with custom events included
    
    Returns:
        Historical data with custom surge events
    """
    base_data = generate_historical_data(365)
    return add_custom_events(base_data, CUSTOM_EVENTS)

# Made with Bob
