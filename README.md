# Health AI API

A simple FastAPI-based health AI service that provides health risk assessment based on basic health metrics. The API includes integrated Swagger documentation and uses machine learning to predict health risks.

## Features

- **Health Risk Prediction**: Analyzes health metrics to predict risk levels (Low, Medium, High)
- **Personalized Recommendations**: Provides tailored health advice based on input data
- **Swagger Integration**: Interactive API documentation at `/docs`
- **REDoc Documentation**: Alternative documentation at `/redoc`
- **Health Check Endpoint**: System health monitoring
- **Input Validation**: Comprehensive validation with appropriate error messages

## Requirements

- Python 3.11+
- FastAPI
- Scikit-learn
- NumPy
- Pandas
- Uvicorn

## Installation

### Option 1: Using pip (Recommended)
```bash
# Install core dependencies
pip3 install fastapi uvicorn pydantic python-multipart requests numpy --break-system-packages
```

### Option 2: Using requirements.txt (if available)
```bash
pip3 install -r requirements.txt --break-system-packages
```

## Usage

### Starting the Server

#### Method 1: Using the startup script
```bash
chmod +x start_server.sh
./start_server.sh
```

#### Method 2: Direct Python execution
```bash
python3 main.py
```

The server will start on `http://localhost:8000`

### Accessing the API

- **API Base URL**: http://localhost:8000
- **Interactive Swagger Documentation**: http://localhost:8000/docs
- **Alternative ReDoc Documentation**: http://localhost:8000/redoc

### API Endpoints

#### 1. Root Endpoint
- **URL**: `GET /`
- **Description**: Welcome message with API information

#### 2. Health Prediction
- **URL**: `POST /predict-health-risk`
- **Description**: Predict health risk based on health metrics
- **Input**: JSON object with health metrics
- **Output**: Risk assessment with recommendations

#### 3. Health Check
- **URL**: `GET /health`
- **Description**: API health status

### Example Request

```bash
curl -X POST "http://localhost:8000/predict-health-risk" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 45,
       "bmi": 25.5,
       "systolic_bp": 120,
       "diastolic_bp": 80,
       "cholesterol": 200,
       "glucose": 90,
       "smoking": false,
       "exercise_hours": 3.5
     }'
```

### Example Response

```json
{
  "risk_level": "Low",
  "risk_score": 0.7,
  "recommendations": [
    "Maintain your current healthy lifestyle!"
  ],
  "confidence": 0.85
}
```

## Health Metrics Input

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| age | int | 1-120 | Age in years |
| bmi | float | 10.0-50.0 | Body Mass Index |
| systolic_bp | int | 70-250 | Systolic blood pressure |
| diastolic_bp | int | 40-150 | Diastolic blood pressure |
| cholesterol | int | 100-400 | Total cholesterol level |
| glucose | int | 50-300 | Blood glucose level |
| smoking | bool | true/false | Smoking status |
| exercise_hours | float | 0.0-20.0 | Exercise hours per week |

## Testing

Run the test script to verify the API:

```bash
python test_api.py
```

## Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Disclaimer

This is a demonstration AI model and should not be used for actual medical diagnosis. Always consult with healthcare professionals for medical advice.

## Development

### AI Implementation

This Health AI uses a **rule-based system** rather than machine learning, making it:
- **Transparent**: All risk calculations are based on established medical guidelines
- **Explainable**: Each recommendation can be traced to specific health metrics
- **Reliable**: No training data bias or model drift concerns
- **Fast**: Instant predictions without complex computations

### Health Risk Factors Considered

The AI evaluates risk based on established medical thresholds:

#### Age-Related Risk
- Moderate risk: 45+ years
- High risk: 65+ years

#### BMI Categories
- Underweight: < 18.5
- Normal: 18.5-24.9
- Overweight: 25.0-29.9
- Obese: ≥ 30.0

#### Blood Pressure (Systolic/Diastolic)
- Normal: < 120/80 mmHg
- Elevated: 120-129/80 mmHg
- Stage 1 Hypertension: 130-139/80-89 mmHg
- Stage 2 Hypertension: ≥ 140/90 mmHg

#### Cholesterol Levels
- Desirable: < 200 mg/dL
- Borderline High: 200-239 mg/dL
- High: ≥ 240 mg/dL

#### Blood Glucose
- Normal: < 100 mg/dL
- Prediabetic: 100-125 mg/dL
- Diabetic: ≥ 126 mg/dL

#### Lifestyle Factors
- **Smoking**: Significant cardiovascular risk multiplier
- **Exercise**: Minimum 150 minutes/week recommended (protective factor)

## License

This project is for educational and demonstration purposes.