"""
Machine Learning module for MediFlow OS
Provides patient surge prediction and analytics
"""

from .surge_model import (
    SurgePredictor,
    get_surge_predictor,
    generate_mock_forecast
)

__all__ = [
    'SurgePredictor',
    'get_surge_predictor',
    'generate_mock_forecast'
]

# Made with Bob
