import requests
import json

# Test the actual API
test_cases = [
    {
        "name": "Bad Code",
        "input": "user_email = request.form['email']\nstore_data_forever(user_email)\nsend_to_third_party(user_email)"
    },
    {
        "name": "Good Code", 
        "input": "if user_consent_given():\n    encrypted_data = encrypt(user_data)\n    store_with_expiry(encrypted_data, 30)"
    }
]

for test in test_cases:
    print(f"\n=== Testing: {test['name']} ===")
    print(f"Input: {test['input']}")
    
    try:
        response = requests.post(
            "http://localhost:8001/analyze",
            json={
                "input_text": test['input'],
                "analysis_type": "gdpr"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result['status']}")
            print(f"Summary: {result['violation_summary']}")
            print(f"Evidence: {result['evidence']}")
            print(f"Grade: {result.get('compliance_grade', {}).get('letter_grade', 'N/A')}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")