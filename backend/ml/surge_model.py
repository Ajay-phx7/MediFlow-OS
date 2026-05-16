import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from prophet import Prophet
from ml.training_data import generate_training_data, generate_india_holidays, generate_flu_spike_events


# Module-level singleton to cache the trained model
_forecaster = None


class SurgeForecaster:
    """
    Time-series forecasting using Facebook Prophet.
    Trained on 6 months of synthetic patient volume data.
    """
    
    def __init__(self):
        """Initialize and train the Prophet model on synthetic data."""
        print("Initializing SurgeForecaster with Prophet...")
        
        # Generate synthetic training data
        self.training_data = generate_training_data()
        
        # Initialize Prophet with appropriate parameters
        # Note: Prophet accepts bool or 'auto' for seasonality parameters
        self.model = Prophet(
            yearly_seasonality=False,    # type: ignore  # Only 6 months data, not enough
            weekly_seasonality=True,     # type: ignore  # Strong weekly pattern exists
            daily_seasonality=False,     # type: ignore  # Not tracking hourly
            interval_width=0.95,         # 95% confidence interval
            seasonality_mode='additive'  # Additive pattern (not multiplicative)
        )
        
        # Add India holidays for better prediction accuracy
        india_holidays = generate_india_holidays()
        for holiday in india_holidays:
            self.model.add_country_holidays(country_name='IN')
        
        # Add custom events (flu spikes, etc.)
        flu_events = generate_flu_spike_events()
        if not flu_events.empty:
            # Add flu spike events to the training data
            self.training_data = pd.merge(
                self.training_data,
                flu_events[['ds', 'flu_spike']],
                on='ds',
                how='left'
            )
            self.training_data['flu_spike'] = self.training_data['flu_spike'].fillna(0)
            
            # Add flu_spike as a regressor
            self.model.add_regressor('flu_spike')
        
        # Suppress Prophet's verbose output
        import logging
        logging.getLogger('prophet').setLevel(logging.WARNING)
        logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
        
        # Train the model
        # NOTE: In production, retrain weekly with new data to maintain accuracy
        # Current implementation: train once on server startup
        print(f"Training Prophet model on {len(self.training_data)} days of data...")
        self.model.fit(self.training_data)
        
        self.last_trained = datetime.now().strftime("%Y-%m-%d")
        print(f"Prophet model trained successfully on {len(self.training_data)} days of data")
        print(f"Training date range: {self.training_data['ds'].min().strftime('%Y-%m-%d')} to {self.training_data['ds'].max().strftime('%Y-%m-%d')}")
        
        # Calculate and store accuracy metrics
        self._calculate_accuracy_metrics()
    
    def _calculate_accuracy_metrics(self):
        """Calculate MAPE and RMSE on training data for model transparency."""
        train_predictions = self.model.predict(self.training_data)
        actual = np.array(self.training_data['y'].values)
        predicted = np.array(train_predictions['yhat'].values)
        
        # MAPE (Mean Absolute Percentage Error)
        self.mape = float(np.mean(np.abs((actual - predicted) / actual)) * 100)
        
        # RMSE (Root Mean Squared Error)
        self.rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))
        
        print(f"Model Accuracy Metrics:")
        print(f"  MAPE: {self.mape:.2f}%")
        print(f"  RMSE: {self.rmse:.2f} patients/day")
    
    def generate_forecast(self, days: int) -> dict:
        """
        Generate future forecast using trained Prophet model.
        
        Args:
            days: Number of days to forecast (7, 14, 30, etc)
        
        Returns:
            dict with structure:
            {
              "dates": ["2024-05-17", "2024-05-18", ...],
              "predicted": [142, 156, 149, ...],
              "upper": [165, 178, 171, ...],
              "lower": [119, 134, 127, ...],
              "threshold": 120,
              "model_info": {
                "model_type": "Prophet (Time-Series)",
                "training_days": 180,
                "last_trained": "2024-05-16",
                "seasonality": ["weekly"],
                "accuracy_mape": 12.5
              }
            }
        """
        try:
            # Create future dataframe for prediction
            future = self.model.make_future_dataframe(periods=days, freq='D')
            
            # Add flu_spike regressor for future dates (set to 0 for normal prediction)
            if 'flu_spike' in self.training_data.columns:
                future['flu_spike'] = 0
            
            # Generate predictions
            forecast = self.model.predict(future)
            
            # Extract only the future predictions (not historical)
            future_forecast = forecast.tail(days)
            
            # Extract relevant columns and convert to lists
            dates = future_forecast['ds'].dt.strftime('%Y-%m-%d').tolist()
            predicted = future_forecast['yhat'].apply(lambda x: int(round(x))).tolist()
            upper = future_forecast['yhat_upper'].apply(lambda x: int(round(x))).tolist()
            lower = future_forecast['yhat_lower'].apply(lambda x: max(0, int(round(x)))).tolist()
            
            print(f"Generated {days}-day forecast (MAPE={self.mape:.1f}%, RMSE={self.rmse:.1f})")
            
            return {
                "dates": dates,
                "predicted": predicted,
                "upper": upper,
                "lower": lower,
                "threshold": 120,
                "model_info": {
                    "model_type": "Prophet (Time-Series)",
                    "training_days": len(self.training_data),
                    "last_trained": self.last_trained,
                    "seasonality": ["weekly", "holidays"],
                    "accuracy_mape": round(self.mape, 1),
                    "accuracy_rmse": round(self.rmse, 1),
                    "features": ["weekly_pattern", "india_holidays", "flu_events"]
                }
            }
        
        except Exception as e:
            print(f"Error generating forecast: {e}")
            print("Falling back to mock data for graceful degradation")
            
            # Fallback to simple mock data if Prophet fails
            today = datetime.now()
            dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
            predicted = [120 + int(10 * np.sin(2 * np.pi * i / 7)) for i in range(days)]
            upper = [p + 20 for p in predicted]
            lower = [max(0, p - 20) for p in predicted]
            
            return {
                "dates": dates,
                "predicted": predicted,
                "upper": upper,
                "lower": lower,
                "threshold": 120,
                "model_info": {
                    "model_type": "Fallback (Mock)",
                    "training_days": 0,
                    "last_trained": datetime.now().strftime("%Y-%m-%d"),
                    "seasonality": ["none"],
                    "accuracy_mape": 0.0
                }
            }


def get_forecaster() -> SurgeForecaster:
    """
    Get or create the singleton SurgeForecaster instance.
    This ensures the model is trained only once on first request.
    """
    global _forecaster
    if _forecaster is None:
        _forecaster = SurgeForecaster()
    return _forecaster


# Backward compatibility: keep the old function signature
def generate_forecast(days: int) -> dict:
    """
    Generate surge forecast using Prophet model.
    This function maintains backward compatibility with existing code.
    
    Args:
        days: Number of days to forecast
        
    Returns:
        Dictionary with dates, predicted values, upper/lower bounds, and threshold
    """
    forecaster = get_forecaster()
    return forecaster.generate_forecast(days)


# Made with Bob
