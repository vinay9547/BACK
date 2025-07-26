#!/usr/bin/env python3
"""
Test script for the Health AI Assistant API
Demonstrates how to interact with the health advice endpoint
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_advice():
    """Test the health advice endpoint with various examples"""
    
    # Test cases
    test_cases = [
        {
            "name": "Simple headache",
            "data": {
                "symptoms": ["headache"],
                "age": 25,
                "severity": "mild"
            }
        },
        {
            "name": "Multiple symptoms with high severity",
            "data": {
                "symptoms": ["fever", "cough", "fatigue"],
                "age": 45,
                "severity": "severe"
            }
        },
        {
            "name": "Elderly patient with chest pain",
            "data": {
                "symptoms": ["chest pain"],
                "age": 70,
                "severity": "moderate"
            }
        },
        {
            "name": "Unknown symptom",
            "data": {
                "symptoms": ["weird feeling"],
                "age": 30
            }
        }
    ]
    
    print("🏥 Health AI Assistant - API Test\n")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"{BASE_URL}/health-advice",
                json=test_case["data"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status: Success")
                print(f"💡 Advice: {result['advice']}")
                print(f"🔥 Urgency: {result['urgency_level'].upper()}")
                print(f"📝 Recommendations: {len(result['recommendations'])} items")
                
                # Show first few recommendations
                for j, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"   {j}. {rec}")
                if len(result['recommendations']) > 3:
                    print(f"   ... and {len(result['recommendations']) - 3} more")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to the server.")
            print("Make sure the FastAPI server is running on http://localhost:8000")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n🌐 Testing Root Endpoint")
    print("-" * 25)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            result = response.json()
            print("✅ Root endpoint working")
            print(f"📄 Message: {result['message']}")
            print("🔗 Available endpoints:")
            for name, path in result['endpoints'].items():
                print(f"   • {name}: {path}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health_check():
    """Test the health check endpoint"""
    print("\n❤️  Testing Health Check")
    print("-" * 22)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            print(f"📊 Status: {result['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Health AI Assistant API Tests...\n")
    
    # Test all endpoints
    test_root_endpoint()
    test_health_check()
    test_health_advice()
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")
    print("\n📖 To explore the API interactively:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")