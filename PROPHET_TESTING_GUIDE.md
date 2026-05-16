# Prophet ML Model Testing Guide

Comprehensive guide for testing the Facebook Prophet-based patient surge prediction model in MediFlow OS.

## Overview

The surge prediction model uses Facebook Prophet, a time series forecasting library developed by Meta, to predict patient volume surges in hospital departments. This guide covers installation, testing, and validation of the model.

## Prerequisites

### Required Packages

```bash
pip install prophet pandas numpy
```

### System Requirements

- Python 3.8+
- 2GB+ RAM for model training
- C++ compiler (for Prophet installation)

## Model Architecture

### Components

1. **SurgePredictor** (`ml/surge_model.py`)
   - Main prediction class
   - Handles model training and forecasting
   - Provides surge threshold analysis

2. **Training Data Generator** (`ml/training_data.py`)
   - Generates synthetic historical data
   - Includes seasonal patterns
   - Simulates surge events

## Testing Procedures

### 1. Basic Model Testing

#### Test Model Initialization

```python
from ml.surge_model import SurgePredictor

# Create predictor instance
predictor = SurgePredictor()

# Check initial state
assert predictor.is_trained == False
assert predictor.model is None
print("✓ Model initialization successful")
```

#### Test Data Preparation

```python
from ml.training_data import generate_historical_data

# Generate test data
data = generate_historical_data(days=90)

# Validate data structure
assert len(data) == 90
assert all('date' in record and 'patient_count' in record for record in data)
print(f"✓ Generated {len(data)} days of training data")
```

### 2. Model Training

#### Train with Historical Data

```python
from ml.surge_model import get_surge_predictor
from ml.training_data import get_training_data

# Get predictor instance
predictor = get_surge_predictor()

# Get training data (1 year)
training_data = get_training_data()
print(f"Training with {len(training_data)} data points...")

# Train the model
predictor.train(training_data)

# Verify training
assert predictor.is_trained == True
assert predictor.model is not None
print("✓ Model training successful")
```

#### Training with Custom Parameters

```python
# Train with custom Prophet parameters
predictor.train(
    training_data,
    changepoint_prior_scale=0.1,  # Flexibility of trend changes
    seasonality_prior_scale=15.0,  # Strength of seasonality
    yearly_seasonality=True,
    weekly_seasonality=True
)
print("✓ Custom parameter training successful")
```

### 3. Making Predictions

#### Basic Prediction

```python
# Predict next 7 days
forecast = predictor.predict(days_ahead=7)

# Validate forecast structure
assert 'dates' in forecast
assert 'predicted' in forecast
assert len(forecast['dates']) == 7
assert len(forecast['predicted']) == 7

print("✓ Basic prediction successful")
print(f"Forecast dates: {forecast['dates']}")
print(f"Predicted counts: {forecast['predicted']}")
```

#### Prediction with Threshold Analysis

```python
# Predict with surge threshold
forecast = predictor.predict_with_threshold(
    days_ahead=7,
    threshold=120
)

# Check surge detection
print(f"Surge alert: {forecast['surge_alert']}")
print(f"Surge days: {len(forecast['surge_days'])}")

if forecast['surge_days']:
    for surge in forecast['surge_days']:
        print(f"  - {surge['date']}: {surge['predicted_count']} patients "
              f"({surge['excess']} over threshold)")
```

### 4. Validation Tests

#### Test Prediction Accuracy

```python
from datetime import datetime, timedelta

# Split data into train/test
train_data = training_data[:-30]  # All but last 30 days
test_data = training_data[-30:]   # Last 30 days

# Train on partial data
predictor.train(train_data)

# Predict the test period
forecast = predictor.predict(days_ahead=30)

# Calculate error metrics
actual_values = [d['patient_count'] for d in test_data]
predicted_values = forecast['predicted']

# Mean Absolute Error
mae = sum(abs(a - p) for a, p in zip(actual_values, predicted_values)) / len(actual_values)
print(f"Mean Absolute Error: {mae:.2f} patients")

# Mean Absolute Percentage Error
mape = sum(abs((a - p) / a) for a, p in zip(actual_values, predicted_values)) / len(actual_values) * 100
print(f"Mean Absolute Percentage Error: {mape:.2f}%")
```

#### Test Seasonality Detection

```python
# Check if model captures weekly patterns
forecast = predictor.predict(days_ahead=14)

# Weekend vs Weekday analysis
from datetime import datetime
weekend_counts = []
weekday_counts = []

for date_str, count in zip(forecast['dates'], forecast['predicted']):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    if date.weekday() >= 5:  # Weekend
        weekend_counts.append(count)
    else:  # Weekday
        weekday_counts.append(count)

avg_weekend = sum(weekend_counts) / len(weekend_counts) if weekend_counts else 0
avg_weekday = sum(weekday_counts) / len(weekday_counts) if weekday_counts else 0

print(f"Average weekend patients: {avg_weekend:.0f}")
print(f"Average weekday patients: {avg_weekday:.0f}")
print(f"Weekend reduction: {((avg_weekday - avg_weekend) / avg_weekday * 100):.1f}%")
```

### 5. Edge Case Testing

#### Test with Minimal Data

```python
# Test with only 30 days of data
minimal_data = generate_historical_data(days=30)
predictor_minimal = SurgePredictor()

try:
    predictor_minimal.train(minimal_data)
    forecast = predictor_minimal.predict(days_ahead=7)
    print("✓ Minimal data test passed")
except Exception as e:
    print(f"✗ Minimal data test failed: {e}")
```

#### Test with Custom Events

```python
from ml.training_data import add_custom_events, CUSTOM_EVENTS

# Add custom surge events
data_with_events = add_custom_events(training_data, CUSTOM_EVENTS)

# Train and predict
predictor.train(data_with_events)
forecast = predictor.predict_with_threshold(days_ahead=7, threshold=120)

print("✓ Custom events test passed")
```

#### Test Error Handling

```python
# Test prediction before training
untrained_predictor = SurgePredictor()
try:
    untrained_predictor.predict(days_ahead=7)
    print("✗ Should have raised error for untrained model")
except ValueError as e:
    print(f"✓ Correctly raised error: {e}")
```

### 6. Performance Testing

#### Test Training Time

```python
import time

# Measure training time
start_time = time.time()
predictor.train(training_data)
training_time = time.time() - start_time

print(f"Training time: {training_time:.2f} seconds")
assert training_time < 30, "Training took too long"
print("✓ Performance test passed")
```

#### Test Prediction Speed

```python
# Measure prediction time
start_time = time.time()
forecast = predictor.predict(days_ahead=30)
prediction_time = time.time() - start_time

print(f"Prediction time: {prediction_time:.2f} seconds")
assert prediction_time < 5, "Prediction took too long"
print("✓ Prediction speed test passed")
```

## Integration Testing

### Test with FastAPI Endpoint

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test surge forecast endpoint
response = client.get("/api/admin/surge-forecast")
assert response.status_code == 200

data = response.json()
assert 'dates' in data
assert 'predicted' in data
assert 'threshold' in data

print("✓ API integration test passed")
```

### Test Mock Forecast Generation

```python
from ml.surge_model import generate_mock_forecast

# Generate mock data (for when model isn't trained)
mock_forecast = generate_mock_forecast(days_ahead=7, threshold=120)

assert len(mock_forecast['dates']) == 7
assert len(mock_forecast['predicted']) == 7
assert 'surge_alert' in mock_forecast

print("✓ Mock forecast generation passed")
```

## Validation Checklist

- [ ] Model initializes correctly
- [ ] Training data generates properly
- [ ] Model trains without errors
- [ ] Predictions return expected format
- [ ] Surge threshold detection works
- [ ] Confidence intervals are reasonable
- [ ] Seasonality patterns are captured
- [ ] Custom events are handled
- [ ] Error handling works correctly
- [ ] Performance meets requirements
- [ ] API integration works
- [ ] Mock data fallback works

## Common Issues and Solutions

### Issue: Prophet Installation Fails

**Solution:**
```bash
# Windows
pip install pystan==2.19.1.1
pip install prophet

# macOS/Linux with conda
conda install -c conda-forge prophet
```

### Issue: Training Takes Too Long

**Solution:**
- Reduce training data size (use 90-180 days instead of 365)
- Adjust Prophet parameters:
  ```python
  predictor.train(data, mcmc_samples=0)  # Disable MCMC sampling
  ```

### Issue: Predictions Are Unrealistic

**Solution:**
- Check training data quality
- Adjust seasonality parameters
- Add more historical data
- Include custom events for known patterns

### Issue: Memory Errors

**Solution:**
- Reduce data size
- Use smaller fourier_order for seasonalities
- Process in batches

## Best Practices

1. **Training Frequency**
   - Retrain weekly with new data
   - Keep at least 6 months of historical data

2. **Threshold Selection**
   - Set threshold at 80-90% of maximum capacity
   - Adjust based on department-specific needs

3. **Validation**
   - Always validate predictions against actual data
   - Monitor prediction accuracy over time
   - Adjust model parameters as needed

4. **Production Use**
   - Cache predictions to reduce computation
   - Implement fallback to mock data
   - Log prediction accuracy for monitoring

## Example Test Script

Complete test script (`test_surge_model.py`):

```python
#!/usr/bin/env python3
"""Complete test suite for surge prediction model"""

from ml.surge_model import get_surge_predictor, generate_mock_forecast
from ml.training_data import get_training_data

def run_all_tests():
    print("Starting surge model tests...\n")
    
    # Test 1: Model initialization
    print("Test 1: Model Initialization")
    predictor = get_surge_predictor()
    assert not predictor.is_trained
    print("✓ Passed\n")
    
    # Test 2: Data generation
    print("Test 2: Training Data Generation")
    data = get_training_data()
    assert len(data) == 365
    print(f"✓ Passed - Generated {len(data)} days\n")
    
    # Test 3: Model training
    print("Test 3: Model Training")
    predictor.train(data)
    assert predictor.is_trained
    print("✓ Passed\n")
    
    # Test 4: Predictions
    print("Test 4: Making Predictions")
    forecast = predictor.predict_with_threshold(days_ahead=7, threshold=120)
    assert len(forecast['dates']) == 7
    print(f"✓ Passed - Predicted {len(forecast['dates'])} days\n")
    
    # Test 5: Mock forecast
    print("Test 5: Mock Forecast Generation")
    mock = generate_mock_forecast(days_ahead=7)
    assert len(mock['dates']) == 7
    print("✓ Passed\n")
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    run_all_tests()
```

Run with:
```bash
python test_surge_model.py
```

## Monitoring in Production

### Key Metrics to Track

1. **Prediction Accuracy**
   - Daily comparison of predicted vs actual
   - Rolling 7-day MAE
   - Alert if accuracy drops below threshold

2. **Model Performance**
   - Training time
   - Prediction latency
   - Memory usage

3. **Business Metrics**
   - Surge detection rate
   - False positive rate
   - Time to surge alert

## Further Reading

- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Time Series Forecasting Best Practices](https://facebook.github.io/prophet/docs/quick_start.html)
- [Prophet Paper](https://peerj.com/preprints/3190/)

## Support

For issues with the surge prediction model:
1. Check this testing guide
2. Review [PROPHET_IMPLEMENTATION_SUMMARY.md](PROPHET_IMPLEMENTATION_SUMMARY.md)
3. Consult Prophet documentation
4. Open an issue with test results