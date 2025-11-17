import requests
import json

BACKEND_URL = "http://127.0.0.1:5000/register" 
TEST_USER_EMAIL = "admin@smarteye.com"
TEST_USER_PASSWORD = "SuperSecurePassword123"

def register_test_user():
    """Sends a registration request to the backend."""
    
    registration_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    print(f"Attempting to register user: {TEST_USER_EMAIL}")
    print(f"Target URL: {BACKEND_URL}")

    try:
        response = requests.post(BACKEND_URL, json=registration_data)
        response.raise_for_status()
        
        result = response.json()
        
        if response.status_code in [201, 200]:
            print("\n--- Registration Successful! ---")
            print(f"Message: {result.get('message')}")
            print(f"User ID: {result.get('user_id')}")
            print("You can now proceed to implement the login endpoint.")
        else:
            print(f"\n--- Registration Failed (HTTP {response.status_code}) ---")
            print(f"Response: {result.get('message')}")

    except requests.exceptions.RequestException as e:
        print(f"\n--- ERROR: Could not connect or post data ---")
        print("Details: Ensure 'backend.py' is running and accessible at http://127.0.0.1:5000")
        print(f"Error: {e}")

if __name__ == '__main__':
    register_test_user()