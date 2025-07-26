from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import re
from datetime import datetime

app = FastAPI(
    title="Health AI API",
    description="A simple Health AI service that provides health recommendations based on symptoms",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # Alternative documentation
)

# Pydantic models for request/response
class SymptomInput(BaseModel):
    symptoms: List[str] = Field(..., description="List of symptoms experienced by the user", example=["headache", "fever", "fatigue"])
    age: Optional[int] = Field(None, description="Age of the user", example=30, ge=1, le=120)
    severity: Optional[int] = Field(None, description="Severity of symptoms on a scale of 1-10", example=5, ge=1, le=10)

class HealthRecommendation(BaseModel):
    assessment: str = Field(..., description="Health assessment based on symptoms")
    recommendations: List[str] = Field(..., description="List of health recommendations")
    urgency_level: str = Field(..., description="Urgency level: low, medium, high, emergency")
    disclaimer: str = Field(..., description="Medical disclaimer")
    timestamp: str = Field(..., description="Timestamp of the assessment")

# Simple health knowledge base
SYMPTOM_PATTERNS = {
    "emergency": {
        "keywords": ["chest pain", "difficulty breathing", "severe bleeding", "unconscious", "stroke", "heart attack"],
        "recommendations": [
            "Seek immediate emergency medical attention",
            "Call emergency services (911) immediately",
            "Do not delay medical care"
        ]
    },
    "high": {
        "keywords": ["high fever", "severe headache", "persistent vomiting", "severe pain", "difficulty swallowing"],
        "recommendations": [
            "Consult a healthcare provider within 24 hours",
            "Monitor symptoms closely",
            "Consider urgent care if symptoms worsen"
        ]
    },
    "medium": {
        "keywords": ["fever", "headache", "nausea", "fatigue", "muscle aches", "sore throat"],
        "recommendations": [
            "Rest and stay hydrated",
            "Monitor symptoms for 2-3 days",
            "Consider over-the-counter pain relievers if appropriate",
            "Consult healthcare provider if symptoms persist or worsen"
        ]
    },
    "low": {
        "keywords": ["mild headache", "minor fatigue", "slight congestion", "mild muscle soreness"],
        "recommendations": [
            "Get adequate rest",
            "Stay hydrated",
            "Consider gentle exercise or stretching",
            "Monitor symptoms"
        ]
    }
}

def analyze_symptoms(symptoms: List[str], age: Optional[int] = None, severity: Optional[int] = None) -> HealthRecommendation:
    """
    Simple AI-like analysis of symptoms to provide health recommendations
    """
    # Convert symptoms to lowercase for matching
    normalized_symptoms = [symptom.lower().strip() for symptom in symptoms]
    
    # Determine urgency level based on symptom patterns
    urgency_level = "low"
    matched_recommendations = set()
    
    # Check for emergency symptoms
    for symptom in normalized_symptoms:
        for emergency_keyword in SYMPTOM_PATTERNS["emergency"]["keywords"]:
            if emergency_keyword in symptom:
                urgency_level = "emergency"
                matched_recommendations.update(SYMPTOM_PATTERNS["emergency"]["recommendations"])
                break
        if urgency_level == "emergency":
            break
    
    # Check for high urgency symptoms
    if urgency_level != "emergency":
        for symptom in normalized_symptoms:
            for high_keyword in SYMPTOM_PATTERNS["high"]["keywords"]:
                if high_keyword in symptom:
                    urgency_level = "high"
                    matched_recommendations.update(SYMPTOM_PATTERNS["high"]["recommendations"])
                    break
    
    # Check for medium urgency symptoms
    if urgency_level not in ["emergency", "high"]:
        for symptom in normalized_symptoms:
            for medium_keyword in SYMPTOM_PATTERNS["medium"]["keywords"]:
                if medium_keyword in symptom:
                    urgency_level = "medium"
                    matched_recommendations.update(SYMPTOM_PATTERNS["medium"]["recommendations"])
                    break
    
    # If no specific patterns matched, use low urgency
    if not matched_recommendations:
        matched_recommendations.update(SYMPTOM_PATTERNS["low"]["recommendations"])
    
    # Adjust based on severity score
    if severity and severity >= 8:
        if urgency_level == "low":
            urgency_level = "medium"
        elif urgency_level == "medium":
            urgency_level = "high"
    
    # Adjust based on age (elderly patients need more attention)
    if age and age >= 65 and urgency_level == "low":
        urgency_level = "medium"
        matched_recommendations.add("Consider consulting healthcare provider due to age-related risk factors")
    
    # Generate assessment
    assessment = f"Based on the reported symptoms ({', '.join(symptoms)}), "
    if severity:
        assessment += f"with severity level {severity}/10, "
    if age:
        assessment += f"for a {age}-year-old patient, "
    
    assessment += f"the urgency level is assessed as {urgency_level}."
    
    return HealthRecommendation(
        assessment=assessment,
        recommendations=list(matched_recommendations),
        urgency_level=urgency_level,
        disclaimer="This is not a substitute for professional medical advice. Always consult healthcare providers for medical concerns.",
        timestamp=datetime.now().isoformat()
    )

@app.get("/")
async def root():
    """
    Root endpoint providing API information
    """
    return {
        "message": "Welcome to Health AI API",
        "version": "1.0.0",
        "endpoints": {
            "health_analysis": "/analyze-health",
            "documentation": "/docs",
            "alternative_docs": "/redoc"
        }
    }

@app.post("/analyze-health", response_model=HealthRecommendation)
async def analyze_health(symptom_input: SymptomInput):
    """
    Analyze health symptoms and provide AI-powered recommendations
    
    This endpoint accepts a list of symptoms along with optional age and severity information,
    and returns health recommendations based on a simple AI analysis.
    
    - **symptoms**: List of symptoms (required)
    - **age**: Age of the patient (optional, 1-120)
    - **severity**: Severity level from 1-10 (optional)
    
    Returns recommendations with urgency level and medical disclaimer.
    """
    try:
        if not symptom_input.symptoms:
            raise HTTPException(status_code=400, detail="At least one symptom must be provided")
        
        # Validate symptoms are not empty strings
        valid_symptoms = [s.strip() for s in symptom_input.symptoms if s.strip()]
        if not valid_symptoms:
            raise HTTPException(status_code=400, detail="Please provide valid, non-empty symptoms")
        
        # Perform health analysis
        recommendation = analyze_symptoms(
            symptoms=valid_symptoms,
            age=symptom_input.age,
            severity=symptom_input.severity
        )
        
        return recommendation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint for the API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Health AI API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)