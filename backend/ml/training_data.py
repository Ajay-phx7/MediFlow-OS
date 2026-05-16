import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict


def generate_training_data() -> pd.DataFrame:
    """
    Generate 6 months of synthetic patient volume data.
    Returns DataFrame with 'ds' and 'y' columns ready for Prophet.
    
    Patterns:
    - Weekday avg: 130 patients/day (M-F)
    - Weekend avg: 90 patients/day (Sat-Sun)
    - Weekly seasonality: Mon-Wed high, Thu-Fri medium, Sat-Sun low
    - Trend: Slight upward trend (+0.2 patients/day)
    - Random noise: ±10 patients/day variance
    - Occasional spikes: 2-3 random days with 50% more patients
    """
    # Generate 180 days of historical data (6 months)
    days = 180
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Create date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Initialize data list
    data = []
    
    # Generate spike days (2-3 random days with high volume)
    spike_indices = np.random.choice(range(days), size=3, replace=False)
    
    for i, date in enumerate(dates):
        # Base volume depends on day of week
        day_of_week = date.dayofweek  # 0=Monday, 6=Sunday
        
        if day_of_week < 5:  # Weekday (Mon-Fri)
            base_volume = 130
        else:  # Weekend (Sat-Sun)
            base_volume = 90
        
        # Add slight upward trend (growth over 6 months)
        trend = 0.2 * i
        
        # Add random noise
        noise = np.random.normal(0, 10)
        
        # Calculate volume
        volume = base_volume + trend + noise
        
        # Add spike if this is a spike day
        if i in spike_indices:
            volume *= 1.5  # 50% increase for spike days
        
        # Ensure volume is positive and reasonable
        volume = max(50, min(300, volume))
        
        data.append({
            'ds': date,
            'y': int(round(volume))
        })
    
    df = pd.DataFrame(data)
    
    print(f"Generated {len(df)} days of synthetic training data")
    print(f"Date range: {df['ds'].min().strftime('%Y-%m-%d')} to {df['ds'].max().strftime('%Y-%m-%d')}")
    print(f"Volume range: {df['y'].min()} to {df['y'].max()} patients/day")
    print(f"Average volume: {df['y'].mean():.1f} patients/day")
    
    return df


def generate_india_holidays() -> List[Dict[str, str]]:
    """
    Generate India holidays for Prophet model.
    Returns list of holiday dictionaries with 'holiday' and 'ds' keys.
    
    Major India holidays that affect hospital patient volume:
    - Diwali (October/November) - 5-day festival
    - Holi (March) - 2-day festival
    - Dussehra (September/October)
    - Eid (varies by lunar calendar)
    - Republic Day (Jan 26)
    - Independence Day (Aug 15)
    - Gandhi Jayanti (Oct 2)
    """
    holidays = []
    
    # Get current year and previous year for 6-month historical data
    current_year = datetime.now().year
    years = [current_year - 1, current_year]
    
    for year in years:
        # Fixed date holidays
        holidays.extend([
            {'holiday': 'republic_day', 'ds': f'{year}-01-26'},
            {'holiday': 'independence_day', 'ds': f'{year}-08-15'},
            {'holiday': 'gandhi_jayanti', 'ds': f'{year}-10-02'},
        ])
        
        # Approximate dates for lunar calendar holidays (simplified)
        # In production, use a proper lunar calendar library
        if year == 2024:
            holidays.extend([
                {'holiday': 'holi', 'ds': '2024-03-25'},
                {'holiday': 'dussehra', 'ds': '2024-10-12'},
                {'holiday': 'diwali', 'ds': '2024-11-01'},
                {'holiday': 'diwali', 'ds': '2024-11-02'},
                {'holiday': 'diwali', 'ds': '2024-11-03'},
            ])
        elif year == 2025:
            holidays.extend([
                {'holiday': 'holi', 'ds': '2025-03-14'},
                {'holiday': 'dussehra', 'ds': '2025-10-02'},
                {'holiday': 'diwali', 'ds': '2025-10-20'},
                {'holiday': 'diwali', 'ds': '2025-10-21'},
                {'holiday': 'diwali', 'ds': '2025-10-22'},
            ])
        elif year == 2026:
            holidays.extend([
                {'holiday': 'holi', 'ds': '2026-03-03'},
                {'holiday': 'dussehra', 'ds': '2026-09-21'},
                {'holiday': 'diwali', 'ds': '2026-11-08'},
                {'holiday': 'diwali', 'ds': '2026-11-09'},
                {'holiday': 'diwali', 'ds': '2026-11-10'},
            ])
    
    return holidays


def generate_flu_spike_events() -> pd.DataFrame:
    """
    Generate custom flu spike events for Prophet model.
    Returns DataFrame with 'ds' and 'flu_spike' columns.
    
    Simulates flu season spikes that typically occur:
    - Winter months (December-February): Higher flu activity
    - Monsoon season (July-August): Increased respiratory infections
    
    flu_spike values:
    - 0: Normal day
    - 1: Flu spike day (adds ~20-30 extra patients)
    """
    # Generate date range for 6 months historical data
    days = 180
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    flu_events = []
    
    for date in dates:
        month = date.month
        flu_spike = 0
        
        # Winter flu season (December, January, February)
        if month in [12, 1, 2]:
            # 30% chance of flu spike during winter
            if np.random.random() < 0.3:
                flu_spike = 1
        
        # Monsoon season (July, August)
        elif month in [7, 8]:
            # 20% chance of flu spike during monsoon
            if np.random.random() < 0.2:
                flu_spike = 1
        
        flu_events.append({
            'ds': date,
            'flu_spike': flu_spike
        })
    
    df = pd.DataFrame(flu_events)
    spike_count = df['flu_spike'].sum()
    print(f"Generated {spike_count} flu spike events in {len(df)} days")
    
    return df


# Made with Bob