#!/usr/bin/env python3
"""
Quick deployment test script for CAEPA
Run this before deployment to verify everything works
"""

import requests
import time
import sys

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not reachable: {e}")
        return False

def test_analyze_endpoint():
    """Test the main analyze endpoint"""
    try:
        test_data = {
            "input_text": "We collect user emails without consent and store them forever",
            "analysis_type": "gdpr"
        }
        response = requests.post("http://localhost:8000/analyze", json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Analyze endpoint working")
            print(f"   Status: {result.get('status')}")
            print(f"   Grade: {result.get('compliance_grade', {}).get('letter_grade', 'N/A')}")
            return True
        else:
            print(f"❌ Analyze endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analyze endpoint error: {e}")
        return False

def test_dashboard_endpoint():
    """Test dashboard endpoint"""
    try:
        response = requests.get("http://localhost:8000/dashboard", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard endpoint working")
            return True
        else:
            print(f"❌ Dashboard endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard endpoint error: {e}")
        return False

def main():
    print("🚀 CAEPA Deployment Test")
    print("=" * 40)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Analyze Endpoint", test_analyze_endpoint),
        ("Dashboard Endpoint", test_dashboard_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()