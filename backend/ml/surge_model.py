"""
Patient Surge Prediction Model using Facebook Prophet
Predicts hospital patient volume surges for capacity planning
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from prophet import Prophet
import numpy as np


class SurgePredictor:
    """Predicts patient surge patterns using Prophet time series forecasting"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.last_training_date = None
        
    def prepare_data(self, historical_data: List[Dict]) -> pd.DataFrame:
        """
        Prepare historical patient data for Prophet
        
        Args:
            historical_data: List of dicts with 'date' and 'patient_count' keys
            
        Returns:
            DataFrame with 'ds' (date) and 'y' (value) columns for Prophet
        """
        df = pd.DataFrame(historical_data)
        df['ds'] = pd.to_datetime(df['date'])
        df['y'] = df['patient_count']
        return df[['ds', 'y']]
    
    def train(self, historical_data: List[Dict], **prophet_params):
        """
        Train the Prophet model on historical patient data
        
        Args:
            historical_data: List of dicts with 'date' and 'patient_count'
            prophet_params: Additional parameters for Prophet model
        """
        df = self.prepare_data(historical_data)
        
        # Initialize Prophet with custom parameters
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0,
            **prophet_params
        )
        
        # Add custom seasonalities for hospital patterns
        self.model.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        )
        
        # Fit the model
        self.model.fit(df)
        self.is_trained = True
        self.last_training_date = datetime.now()
        
    def predict(self, days_ahead: int = 7) -> Dict:
        """
        Generate surge predictions for the specified number of days
        
        Args:
            days_ahead: Number of days to forecast
            
        Returns:
            Dictionary with dates, predictions, and confidence intervals
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=days_ahead)
        
        # Generate forecast
        forecast = self.model.predict(future)
        
        # Extract last N predictions (future dates only)
        future_forecast = forecast.tail(days_ahead)
        
        return {
            'dates': future_forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
            'predicted': future_forecast['yhat'].round().astype(int).tolist(),
            'lower_bound': future_forecast['yhat_lower'].round().astype(int).tolist(),
            'upper_bound': future_forecast['yhat_upper'].round().astype(int).tolist(),
            'trend': future_forecast['trend'].round().astype(int).tolist()
        }
    
    def predict_with_threshold(self, days_ahead: int = 7, threshold: int = 120) -> Dict:
        """
        Generate predictions with surge threshold analysis
        
        Args:
            days_ahead: Number of days to forecast
            threshold: Patient count threshold for surge alert
            
        Returns:
            Dictionary with predictions and surge alerts
        """
        predictions = self.predict(days_ahead)
        
        # Identify surge days
        surge_days = []
        for i, (date, count) in enumerate(zip(predictions['dates'], predictions['predicted'])):
            if count > threshold:
                surge_days.append({
                    'date': date,
                    'predicted_count': count,
                    'excess': count - threshold
                })
        
        return {
            **predictions,
            'threshold': threshold,
            'surge_days': surge_days,
            'surge_alert': len(surge_days) > 0
        }
    
    def get_model_info(self) -> Dict:
        """Get information about the trained model"""
        return {
            'is_trained': self.is_trained,
            'last_training_date': self.last_training_date.isoformat() if self.last_training_date else None,
            'model_type': 'Facebook Prophet'
        }


# Global model instance
_surge_predictor = None


def get_surge_predictor() -> SurgePredictor:
    """Get or create the global surge predictor instance"""
    global _surge_predictor
    if _surge_predictor is None:
        _surge_predictor = SurgePredictor()
    return _surge_predictor


def generate_mock_forecast(days_ahead: int = 7, threshold: int = 120) -> Dict:
    """
    Generate mock forecast data for testing without trained model
    
    Args:
        days_ahead: Number of days to forecast
        threshold: Surge threshold
        
    Returns:
        Mock forecast data
    """
    base_date = datetime.now()
    dates = [(base_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days_ahead)]
    
    # Generate realistic-looking patient counts with some variation
    base_count = 100
    predicted = [
        int(base_count + 20 * np.sin(i * 0.5) + np.random.randint(-10, 20))
        for i in range(days_ahead)
    ]
    
    surge_days = []
    for date, count in zip(dates, predicted):
        if count > threshold:
            surge_days.append({
                'date': date,
                'predicted_count': count,
                'excess': count - threshold
            })
    
    return {
        'dates': dates,
        'predicted': predicted,
        'lower_bound': [max(0, p - 15) for p in predicted],
        'upper_bound': [p + 15 for p in predicted],
        'trend': predicted,
        'threshold': threshold,
        'surge_days': surge_days,
        'surge_alert': len(surge_days) > 0
    }

# Made with Bob
