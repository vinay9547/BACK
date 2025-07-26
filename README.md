# Health AI API

A simple Health AI service built with FastAPI that provides health recommendations based on symptoms analysis.

## Features

- **Single Health Analysis Endpoint**: Analyzes symptoms and provides AI-powered health recommendations
- **Swagger Integration**: Built-in API documentation at `/docs`
- **Urgency Assessment**: Categorizes symptoms into emergency, high, medium, or low urgency levels
- **Age and Severity Consideration**: Takes into account patient age and symptom severity
- **Medical Disclaimer**: Includes appropriate medical disclaimers

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### POST /analyze-health
Analyzes health symptoms and provides recommendations.

**Request Body:**
```json
{
  "symptoms": ["headache", "fever", "fatigue"],
  "age": 30,
  "severity": 5
}
```

**Response:**
```json
{
  "assessment": "Based on the reported symptoms...",
  "recommendations": [
    "Rest and stay hydrated",
    "Monitor symptoms for 2-3 days",
    "Consider over-the-counter pain relievers if appropriate"
  ],
  "urgency_level": "medium",
  "disclaimer": "This is not a substitute for professional medical advice...",
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET /
Root endpoint providing API information.

### GET /health
Health check endpoint for monitoring API status.

## Usage Examples

### Using curl:
```bash
curl -X POST "http://localhost:8000/analyze-health" \
     -H "Content-Type: application/json" \
     -d '{
       "symptoms": ["headache", "fever"],
       "age": 25,
       "severity": 6
     }'
```

### Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze-health",
    json={
        "symptoms": ["sore throat", "mild fever"],
        "age": 30,
        "severity": 4
    }
)
print(response.json())
```

## Urgency Levels

- **Emergency**: Requires immediate medical attention
- **High**: Should consult healthcare provider within 24 hours
- **Medium**: Monitor symptoms and consider medical consultation if they persist
- **Low**: General wellness recommendations

## Important Note

This is a simple demonstration AI and should not be used for actual medical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical concerns.