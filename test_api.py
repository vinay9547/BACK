import requests
import json

# Test data for health prediction
test_cases = [
    {
        "name": "Healthy Individual",
        "data": {
            "age": 30,
            "bmi": 22.5,
            "systolic_bp": 110,
            "diastolic_bp": 70,
            "cholesterol": 180,
            "glucose": 85,
            "smoking": False,
            "exercise_hours": 5.0
        }
    },
    {
        "name": "Medium Risk Individual",
        "data": {
            "age": 45,
            "bmi": 28.0,
            "systolic_bp": 135,
            "diastolic_bp": 85,
            "cholesterol": 220,
            "glucose": 110,
            "smoking": False,
            "exercise_hours": 2.0
        }
    },
    {
        "name": "High Risk Individual",
        "data": {
            "age": 60,
            "bmi": 32.0,
            "systolic_bp": 160,
            "diastolic_bp": 95,
            "cholesterol": 280,
            "glucose": 140,
            "smoking": True,
            "exercise_hours": 0.5
        }
    },
    {
        "name": "Very Healthy Young Adult",
        "data": {
            "age": 25,
            "bmi": 21.0,
            "systolic_bp": 110,
            "diastolic_bp": 70,
            "cholesterol": 180,
            "glucose": 85,
            "smoking": False,
            "exercise_hours": 6.0
        }
    }
]

def test_health_api():
    """Test the health AI API with different scenarios"""
    base_url = "http://localhost:8000"
    
    # Test root endpoint
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root response: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("API server is not running. Start it with: python main.py")
        return
    
    # Test health check
    print("Testing health check...")
    response = requests.get(f"{base_url}/health")
    print(f"Health check: {response.json()}")
    print()
    
    # Test risk factors endpoint
    print("Testing risk factors endpoint...")
    response = requests.get(f"{base_url}/risk-factors")
    if response.status_code == 200:
        risk_factors = response.json()
        print("Risk factors information available:")
        for category, info in risk_factors["risk_factors"].items():
            if isinstance(info, dict) and 'description' in info:
                print(f"  - {category}: {info['description']}")
            else:
                print(f"  - {category}: {info}")
    print()
    
    # Test prediction endpoint with different cases
    print("Testing health prediction endpoint...")
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Input: {json.dumps(test_case['data'], indent=2)}")
        
        response = requests.post(
            f"{base_url}/predict-health-risk",
            json=test_case['data']
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {json.dumps(result, indent=2)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_health_api()