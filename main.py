from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np
import uvicorn

# Initialize FastAPI app with custom OpenAPI info
app = FastAPI(
    title="Health AI API",
    description="A simple AI service for health risk assessment based on basic health metrics",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc endpoint
)

# Pydantic models for request and response
class HealthMetrics(BaseModel):
    age: int = Field(..., ge=1, le=120, description="Age in years")
    bmi: float = Field(..., ge=10.0, le=50.0, description="Body Mass Index")
    systolic_bp: int = Field(..., ge=70, le=250, description="Systolic blood pressure")
    diastolic_bp: int = Field(..., ge=40, le=150, description="Diastolic blood pressure")
    cholesterol: int = Field(..., ge=100, le=400, description="Total cholesterol level")
    glucose: int = Field(..., ge=50, le=300, description="Blood glucose level")
    smoking: bool = Field(..., description="Smoking status (True if smoker)")
    exercise_hours: float = Field(..., ge=0.0, le=20.0, description="Exercise hours per week")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "bmi": 25.5,
                "systolic_bp": 120,
                "diastolic_bp": 80,
                "cholesterol": 200,
                "glucose": 90,
                "smoking": False,
                "exercise_hours": 3.5
            }
        }

class HealthPrediction(BaseModel):
    risk_level: str = Field(..., description="Health risk level: Low, Medium, or High")
    risk_score: float = Field(..., description="Risk score between 0 and 1")
    recommendations: list[str] = Field(..., description="Health recommendations")
    confidence: float = Field(..., description="Model confidence in prediction")

# Simple rule-based health AI model
class HealthAI:
    def __init__(self):
        # Risk thresholds based on medical guidelines
        self.age_risk_threshold = 45
        self.bmi_normal_max = 24.9
        self.bmi_overweight_max = 29.9
        self.systolic_normal_max = 120
        self.systolic_elevated_max = 129
        self.systolic_high_max = 139
        self.diastolic_normal_max = 80
        self.diastolic_elevated_max = 89
        self.cholesterol_normal_max = 200
        self.cholesterol_borderline_max = 239
        self.glucose_normal_max = 100
        self.glucose_prediabetic_max = 125
        self.exercise_recommended_min = 2.5
    
    def calculate_risk_score(self, metrics: HealthMetrics) -> float:
        """Calculate risk score based on health metrics using rule-based logic"""
        risk_factors = []
        
        # Age factor (0-0.15)
        if metrics.age >= 65:
            risk_factors.append(0.15)
        elif metrics.age >= self.age_risk_threshold:
            risk_factors.append(0.10)
        else:
            risk_factors.append(0.02)
        
        # BMI factor (0-0.20)
        if metrics.bmi >= 35:
            risk_factors.append(0.20)
        elif metrics.bmi > self.bmi_overweight_max:
            risk_factors.append(0.15)
        elif metrics.bmi > self.bmi_normal_max:
            risk_factors.append(0.08)
        else:
            risk_factors.append(0.02)
        
        # Blood pressure factor (0-0.25)
        bp_risk = 0
        if metrics.systolic_bp >= 180 or metrics.diastolic_bp >= 110:
            bp_risk = 0.25  # Stage 2 hypertension
        elif metrics.systolic_bp >= 140 or metrics.diastolic_bp >= 90:
            bp_risk = 0.20  # Stage 1 hypertension
        elif metrics.systolic_bp > self.systolic_elevated_max or metrics.diastolic_bp > self.diastolic_elevated_max:
            bp_risk = 0.12  # High blood pressure
        elif metrics.systolic_bp > self.systolic_normal_max or metrics.diastolic_bp > self.diastolic_normal_max:
            bp_risk = 0.05  # Elevated
        else:
            bp_risk = 0.02  # Normal
        risk_factors.append(bp_risk)
        
        # Cholesterol factor (0-0.15)
        if metrics.cholesterol >= 280:
            risk_factors.append(0.15)
        elif metrics.cholesterol > self.cholesterol_borderline_max:
            risk_factors.append(0.12)
        elif metrics.cholesterol > self.cholesterol_normal_max:
            risk_factors.append(0.08)
        else:
            risk_factors.append(0.02)
        
        # Glucose factor (0-0.15)
        if metrics.glucose >= 126:
            risk_factors.append(0.15)  # Diabetic range
        elif metrics.glucose > self.glucose_prediabetic_max:
            risk_factors.append(0.10)  # Prediabetic range
        elif metrics.glucose > self.glucose_normal_max:
            risk_factors.append(0.05)  # Elevated
        else:
            risk_factors.append(0.02)
        
        # Smoking factor (0-0.15)
        if metrics.smoking:
            risk_factors.append(0.15)
        else:
            risk_factors.append(0.0)
        
        # Exercise factor (-0.10 to 0.05)
        if metrics.exercise_hours >= 5:
            risk_factors.append(-0.10)  # Protective factor
        elif metrics.exercise_hours >= self.exercise_recommended_min:
            risk_factors.append(-0.05)  # Some protection
        elif metrics.exercise_hours >= 1:
            risk_factors.append(0.02)
        else:
            risk_factors.append(0.05)  # Sedentary lifestyle risk
        
        # Calculate total risk score
        total_risk = sum(risk_factors)
        
        # Normalize to 0-1 range
        normalized_risk = max(0.0, min(1.0, total_risk))
        
        return normalized_risk
    
    def determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on calculated risk score"""
        if risk_score < 0.3:
            return "Low"
        elif risk_score < 0.6:
            return "Medium"
        else:
            return "High"
    
    def calculate_confidence(self, metrics: HealthMetrics, risk_score: float) -> float:
        """Calculate confidence based on how clear-cut the risk factors are"""
        confidence_factors = []
        
        # Age confidence (older age = higher confidence)
        if metrics.age >= 65 or metrics.age <= 25:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.8)
        
        # BMI confidence
        if metrics.bmi < 18.5 or metrics.bmi > 35:
            confidence_factors.append(0.9)
        elif metrics.bmi > 30 or metrics.bmi < 20:
            confidence_factors.append(0.85)
        else:
            confidence_factors.append(0.8)
        
        # Blood pressure confidence
        if metrics.systolic_bp >= 180 or metrics.systolic_bp <= 90:
            confidence_factors.append(0.95)
        elif metrics.systolic_bp >= 140 or metrics.systolic_bp <= 100:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.8)
        
        # Smoking confidence (clear factor)
        confidence_factors.append(0.95)
        
        # Exercise confidence
        if metrics.exercise_hours >= 7 or metrics.exercise_hours == 0:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.8)
        
        return np.mean(confidence_factors)
    
    def generate_recommendations(self, metrics: HealthMetrics, risk_level: str) -> list[str]:
        """Generate personalized health recommendations"""
        recommendations = []
        
        # BMI recommendations
        if metrics.bmi > 30:
            recommendations.append("Consider weight management through a combination of healthy diet and regular exercise")
        elif metrics.bmi > self.bmi_normal_max:
            recommendations.append("Maintain a healthy weight through balanced nutrition and physical activity")
        elif metrics.bmi < 18.5:
            recommendations.append("Consider consulting a healthcare provider about healthy weight gain strategies")
        
        # Blood pressure recommendations
        if metrics.systolic_bp >= 140 or metrics.diastolic_bp >= 90:
            recommendations.append("Monitor blood pressure regularly and consult a healthcare provider for hypertension management")
        elif metrics.systolic_bp > 120 or metrics.diastolic_bp > 80:
            recommendations.append("Monitor blood pressure and consider lifestyle modifications to prevent hypertension")
        
        # Cholesterol recommendations
        if metrics.cholesterol > 240:
            recommendations.append("Consult a healthcare provider about cholesterol management and consider dietary changes")
        elif metrics.cholesterol > self.cholesterol_normal_max:
            recommendations.append("Consider heart-healthy diet with reduced saturated fats and increased fiber")
        
        # Glucose recommendations
        if metrics.glucose >= 126:
            recommendations.append("Consult a healthcare provider immediately for diabetes management")
        elif metrics.glucose > self.glucose_prediabetic_max:
            recommendations.append("Monitor blood sugar levels and consider lifestyle changes to prevent diabetes")
        elif metrics.glucose > self.glucose_normal_max:
            recommendations.append("Monitor blood glucose and maintain a balanced diet with limited refined sugars")
        
        # Smoking recommendations
        if metrics.smoking:
            recommendations.append("Consider quitting smoking - this is the single most important step for improving health")
        
        # Exercise recommendations
        if metrics.exercise_hours < 1:
            recommendations.append("Gradually increase physical activity to at least 150 minutes of moderate exercise per week")
        elif metrics.exercise_hours < self.exercise_recommended_min:
            recommendations.append("Increase physical activity to meet the recommended 150 minutes per week")
        elif metrics.exercise_hours >= 7:
            recommendations.append("Excellent exercise routine! Continue maintaining your active lifestyle")
        
        # Age-specific recommendations
        if metrics.age >= 50:
            recommendations.append("Consider regular health screenings appropriate for your age group")
        
        # Risk-level specific recommendations
        if risk_level == "High":
            recommendations.append("Schedule a comprehensive health evaluation with your healthcare provider")
        elif risk_level == "Medium":
            recommendations.append("Consider lifestyle modifications and regular health monitoring")
        
        # Default positive recommendation
        if not recommendations:
            recommendations.append("Excellent health profile! Continue maintaining your healthy lifestyle")
        
        return recommendations
    
    def predict(self, metrics: HealthMetrics) -> HealthPrediction:
        """Make health risk prediction"""
        try:
            # Calculate risk score
            risk_score = self.calculate_risk_score(metrics)
            
            # Determine risk level
            risk_level = self.determine_risk_level(risk_score)
            
            # Calculate confidence
            confidence = self.calculate_confidence(metrics, risk_score)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(metrics, risk_level)
            
            return HealthPrediction(
                risk_level=risk_level,
                risk_score=float(risk_score),
                recommendations=recommendations,
                confidence=float(confidence)
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Initialize the health AI model
health_ai = HealthAI()

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to Health AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "description": "Rule-based health risk assessment system"
    }

@app.post("/predict-health-risk", response_model=HealthPrediction, tags=["Health Prediction"])
async def predict_health_risk(metrics: HealthMetrics):
    """
    Predict health risk based on provided health metrics.
    
    This endpoint analyzes various health indicators and provides:
    - Risk level assessment (Low, Medium, High)
    - Risk score (0-1 probability)
    - Personalized health recommendations
    - Model confidence in the prediction
    
    The AI uses rule-based logic based on established medical guidelines for:
    - BMI classification
    - Blood pressure categories
    - Cholesterol levels
    - Blood glucose ranges
    - Age-related risk factors
    - Lifestyle factors (smoking, exercise)
    
    **Note**: This is a demonstration AI model and should not be used for actual medical diagnosis.
    Always consult with healthcare professionals for medical advice.
    """
    try:
        prediction = health_ai.predict(metrics)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health", tags=["System"])
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "service": "Health AI API", "type": "rule-based"}

@app.get("/risk-factors", tags=["Information"])
async def get_risk_factors():
    """Get information about health risk factors considered by the AI"""
    return {
        "risk_factors": {
            "age": {
                "description": "Age-related cardiovascular risk",
                "thresholds": {"moderate_risk": 45, "high_risk": 65}
            },
            "bmi": {
                "description": "Body Mass Index categories",
                "ranges": {
                    "underweight": "< 18.5",
                    "normal": "18.5 - 24.9",
                    "overweight": "25.0 - 29.9",
                    "obese": "≥ 30.0"
                }
            },
            "blood_pressure": {
                "description": "Blood pressure categories (systolic/diastolic)",
                "ranges": {
                    "normal": "< 120/80",
                    "elevated": "120-129/80",
                    "stage_1": "130-139/80-89",
                    "stage_2": "≥ 140/90"
                }
            },
            "cholesterol": {
                "description": "Total cholesterol levels",
                "ranges": {
                    "desirable": "< 200 mg/dL",
                    "borderline": "200-239 mg/dL",
                    "high": "≥ 240 mg/dL"
                }
            },
            "glucose": {
                "description": "Blood glucose levels",
                "ranges": {
                    "normal": "< 100 mg/dL",
                    "prediabetic": "100-125 mg/dL",
                    "diabetic": "≥ 126 mg/dL"
                }
            },
            "lifestyle": {
                "smoking": "Significant cardiovascular risk factor",
                "exercise": "Minimum 150 minutes moderate exercise per week recommended"
            }
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)