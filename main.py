from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# Initialize FastAPI app with metadata for Swagger documentation
app = FastAPI(
    title="Health AI Assistant",
    description="A simple AI-powered health assistant that provides basic health advice based on symptoms",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc endpoint
)

# Pydantic models for request and response
class SymptomRequest(BaseModel):
    symptoms: List[str] = Field(
        ...,
        description="List of symptoms the user is experiencing",
        example=["headache", "fever", "fatigue"]
    )
    age: Optional[int] = Field(
        None,
        description="Age of the person (optional)",
        example=25,
        ge=0,
        le=120
    )
    severity: Optional[str] = Field(
        None,
        description="Severity level of symptoms",
        example="mild",
        pattern="^(mild|moderate|severe)$"
    )

class HealthAdvice(BaseModel):
    advice: str = Field(description="Health advice based on the symptoms")
    recommendations: List[str] = Field(description="List of specific recommendations")
    urgency_level: str = Field(description="Urgency level: low, medium, or high")
    disclaimer: str = Field(description="Medical disclaimer")

# Simple health advice database
HEALTH_DATABASE = {
    "headache": {
        "advice": "Headaches can be caused by various factors including stress, dehydration, or lack of sleep.",
        "recommendations": ["Stay hydrated", "Get adequate rest", "Apply cold or warm compress", "Avoid bright lights"],
        "urgency": "low"
    },
    "fever": {
        "advice": "Fever is often a sign that your body is fighting an infection.",
        "recommendations": ["Stay hydrated", "Rest", "Monitor temperature", "Consider fever-reducing medication"],
        "urgency": "medium"
    },
    "chest pain": {
        "advice": "Chest pain can be serious and may require immediate medical attention.",
        "recommendations": ["Seek immediate medical attention", "Do not ignore persistent chest pain"],
        "urgency": "high"
    },
    "fatigue": {
        "advice": "Fatigue can result from poor sleep, stress, or underlying health conditions.",
        "recommendations": ["Ensure adequate sleep", "Maintain regular exercise", "Eat balanced meals", "Manage stress"],
        "urgency": "low"
    },
    "cough": {
        "advice": "Coughs can be caused by respiratory infections, allergies, or other conditions.",
        "recommendations": ["Stay hydrated", "Use honey for soothing", "Avoid irritants", "Rest your voice"],
        "urgency": "low"
    },
    "nausea": {
        "advice": "Nausea can be caused by various factors including food, stress, or illness.",
        "recommendations": ["Stay hydrated with small sips", "Eat bland foods", "Rest", "Avoid strong odors"],
        "urgency": "low"
    }
}

def analyze_symptoms(symptoms: List[str], age: Optional[int] = None, severity: Optional[str] = None) -> HealthAdvice:
    """
    Analyze symptoms and provide health advice
    """
    found_symptoms = []
    all_recommendations = []
    max_urgency = "low"
    
    # Process each symptom
    for symptom in symptoms:
        symptom_lower = symptom.lower().strip()
        
        # Check if symptom exists in our database
        for key, value in HEALTH_DATABASE.items():
            if key in symptom_lower or symptom_lower in key:
                found_symptoms.append(key)
                all_recommendations.extend(value["recommendations"])
                
                # Update urgency level
                if value["urgency"] == "high":
                    max_urgency = "high"
                elif value["urgency"] == "medium" and max_urgency != "high":
                    max_urgency = "medium"
    
    # Generate advice based on found symptoms
    if not found_symptoms:
        advice = "I don't have specific information about these symptoms. Please consult with a healthcare professional for proper evaluation."
        all_recommendations = ["Consult with a healthcare professional", "Monitor your symptoms", "Seek medical attention if symptoms worsen"]
    else:
        if len(found_symptoms) == 1:
            advice = HEALTH_DATABASE[found_symptoms[0]]["advice"]
        else:
            advice = f"You're experiencing multiple symptoms: {', '.join(found_symptoms)}. This could indicate various conditions."
    
    # Adjust urgency based on severity and age
    if severity == "severe":
        max_urgency = "high"
    elif age and age > 65 and max_urgency != "high":
        max_urgency = "medium"
    
    # Remove duplicates from recommendations
    unique_recommendations = list(dict.fromkeys(all_recommendations))
    
    # Add general recommendations
    if max_urgency == "high":
        unique_recommendations.insert(0, "Seek immediate medical attention")
    else:
        unique_recommendations.append("Monitor your symptoms and consult a healthcare provider if they persist or worsen")
    
    disclaimer = "This advice is for informational purposes only and should not replace professional medical consultation. Always consult with a qualified healthcare provider for proper diagnosis and treatment."
    
    return HealthAdvice(
        advice=advice,
        recommendations=unique_recommendations,
        urgency_level=max_urgency,
        disclaimer=disclaimer
    )

@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint providing API information
    """
    return {
        "message": "Welcome to Health AI Assistant",
        "description": "A simple AI-powered health assistant",
        "endpoints": {
            "health_advice": "/health-advice",
            "documentation": "/docs",
            "redoc": "/redoc"
        }
    }

@app.post("/health-advice", response_model=HealthAdvice, tags=["Health AI"])
async def get_health_advice(request: SymptomRequest):
    """
    Get health advice based on symptoms
    
    This endpoint analyzes the provided symptoms and returns personalized health advice,
    recommendations, and urgency level. The AI considers factors like age and severity
    to provide more accurate guidance.
    
    **Note:** This is not a substitute for professional medical advice.
    """
    try:
        if not request.symptoms:
            raise HTTPException(status_code=400, detail="At least one symptom must be provided")
        
        # Validate symptoms (basic check for meaningful input)
        for symptom in request.symptoms:
            if not symptom.strip():
                raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
        
        advice = analyze_symptoms(request.symptoms, request.age, request.severity)
        return advice
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request: {str(e)}")

@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check endpoint for the API
    """
    return {"status": "healthy", "message": "Health AI Assistant is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)