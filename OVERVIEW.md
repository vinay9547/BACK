# Health AI Assistant - Project Overview

## 🎯 Project Summary

A simple but powerful health AI assistant built with FastAPI that provides basic health advice based on symptoms. The application features automatic Swagger documentation and demonstrates a clean API design for health-related applications.

## 🏗️ Architecture

### Core Components
- **FastAPI Application** (`main.py`) - Main web application with REST API
- **Pydantic Models** - Strong typing and validation for requests/responses  
- **Health Database** - Simple rule-based symptom analysis system
- **Swagger/OpenAPI** - Automatic documentation generation

### Key Features
- ✅ **Single Main Endpoint**: `/health-advice` for symptom analysis
- ✅ **Swagger Integration**: Interactive API documentation at `/docs`
- ✅ **Input Validation**: Pydantic models with field validation
- ✅ **Health Assessment**: Rule-based analysis of common symptoms
- ✅ **Urgency Classification**: Low/Medium/High urgency levels
- ✅ **Age Considerations**: Adjusted recommendations based on age
- ✅ **Severity Factors**: Symptom severity affects urgency assessment

## 📁 Project Structure

```
/workspace/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── test_api.py         # API testing script
├── README.md           # Detailed documentation
├── OVERVIEW.md         # This file
└── health_ai_env/      # Python virtual environment
```

## 🚀 Quick Start

1. **Setup Environment**:
   ```bash
   python3 -m venv health_ai_env
   source health_ai_env/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Application**:
   ```bash
   python main.py
   ```

3. **Access Endpoints**:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔍 API Endpoints

### Primary Endpoint
- **POST /health-advice** - Main health consultation endpoint
  - Input: symptoms, age (optional), severity (optional)
  - Output: advice, recommendations, urgency level, disclaimer

### Support Endpoints  
- **GET /** - Welcome message and endpoint listing
- **GET /health** - Health check for monitoring
- **GET /docs** - Interactive Swagger documentation
- **GET /redoc** - Alternative documentation view

## 💊 Supported Symptoms

The AI currently recognizes and provides advice for:
- Headache
- Fever  
- Chest pain
- Fatigue
- Cough
- Nausea

*Note: Unknown symptoms receive general guidance to consult healthcare professionals.*

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

### Test Coverage
- ✅ Root endpoint functionality
- ✅ Health check endpoint
- ✅ Single symptom analysis
- ✅ Multiple symptom combinations
- ✅ Severity-based urgency escalation
- ✅ Age-factor considerations
- ✅ Unknown symptom handling

## 🛠️ Technical Specifications

### Dependencies
- **FastAPI 0.115.6** - Modern Python web framework
- **Uvicorn 0.32.1** - ASGI server with async support
- **Pydantic 2.10.4** - Data validation and serialization
- **Python 3.13+** - Latest Python version support

### Response Format
All health advice responses include:
```json
{
  "advice": "Detailed health guidance",
  "recommendations": ["List of specific actions"],
  "urgency_level": "low|medium|high", 
  "disclaimer": "Medical disclaimer text"
}
```

### Validation Rules
- **Symptoms**: Required, non-empty list of strings
- **Age**: Optional, 0-120 years range
- **Severity**: Optional, "mild|moderate|severe" pattern

## 🏥 Health Logic

### Urgency Assessment
- **Low**: General symptoms (headache, fatigue, etc.)
- **Medium**: Fever or elderly patients (65+)
- **High**: Severe symptoms, chest pain, or "severe" severity

### Recommendation Engine
1. **Symptom Matching**: Fuzzy matching against known symptoms
2. **Advice Generation**: Specific or general guidance based on matches
3. **Recommendation Aggregation**: Combines relevant suggestions
4. **Urgency Calculation**: Determines priority level
5. **Safety Disclaimer**: Always includes medical consultation advice

## ⚠️ Important Disclaimers

This application is designed for **educational and informational purposes only**:

- 🚫 **Not a substitute** for professional medical advice
- 🚫 **Not for emergency situations** - call emergency services immediately
- 🚫 **Not for diagnosis** - always consult qualified healthcare providers
- 🚫 **Limited symptom database** - many conditions not covered

## 🎓 Educational Value

This project demonstrates:
- Modern Python web API development
- FastAPI framework usage
- Automatic API documentation
- Input validation with Pydantic
- REST API best practices
- Health informatics basics
- Clean code architecture

## 🔮 Future Enhancements

Potential improvements for expanded versions:
- Expanded symptom database
- Integration with medical APIs
- Machine learning for better recommendations
- User history and tracking
- Multilingual support
- Emergency contact integration
- Healthcare provider referrals

---

**Built with ❤️ using FastAPI and Python 3.13**