# Health AI Assistant

A simple AI-powered health assistant built with FastAPI that provides basic health advice based on symptoms. The application features automatic Swagger documentation and a clean API interface.

## Features

- **Single Main Endpoint**: `/health-advice` - Analyzes symptoms and provides health recommendations
- **Swagger Integration**: Automatic API documentation at `/docs`
- **Pydantic Validation**: Strong input validation and type checking
- **Health Database**: Simple rule-based system for common symptoms
- **Urgency Assessment**: Categorizes advice by urgency level (low, medium, high)
- **Age and Severity Factors**: Considers user age and symptom severity for better advice

## API Endpoints

### Main Endpoint
- `POST /health-advice` - Get health advice based on symptoms

### Additional Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

### Via Swagger UI
1. Open your browser and go to `http://localhost:8000/docs`
2. Use the interactive Swagger interface to test the API

### Via curl
```bash
curl -X POST "http://localhost:8000/health-advice" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["headache", "fever"],
    "age": 30,
    "severity": "mild"
  }'
```

### Example Request
```json
{
  "symptoms": ["headache", "fever", "fatigue"],
  "age": 25,
  "severity": "moderate"
}
```

### Example Response
```json
{
  "advice": "You're experiencing multiple symptoms: headache, fever, fatigue. This could indicate various conditions.",
  "recommendations": [
    "Stay hydrated",
    "Get adequate rest",
    "Apply cold or warm compress",
    "Avoid bright lights",
    "Rest",
    "Monitor temperature",
    "Consider fever-reducing medication",
    "Ensure adequate sleep",
    "Maintain regular exercise",
    "Eat balanced meals",
    "Manage stress",
    "Monitor your symptoms and consult a healthcare provider if they persist or worsen"
  ],
  "urgency_level": "medium",
  "disclaimer": "This advice is for informational purposes only and should not replace professional medical consultation. Always consult with a qualified healthcare provider for proper diagnosis and treatment."
}
```

## Supported Symptoms

The AI currently recognizes these symptoms:
- Headache
- Fever
- Chest pain
- Fatigue
- Cough
- Nausea

## Important Disclaimer

This application is for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.

## Technical Details

- **Framework**: FastAPI
- **Python Version**: 3.11+ (tested with 3.13.3)
- **Validation**: Pydantic v2
- **Documentation**: Auto-generated Swagger/OpenAPI
- **Server**: Uvicorn ASGI server

## Development

The application is structured with:
- Input validation using Pydantic models
- Simple rule-based health advice system
- Comprehensive error handling
- Proper HTTP status codes
- Clear API documentation