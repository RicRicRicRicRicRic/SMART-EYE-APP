import requests
import json

BACKEND_URL = "http://127.0.0.1:5000/login" 
TEST_USER_EMAIL = "admin@smarteye.com"
TEST_USER_PASSWORD = "SuperSecurePassword123"

def login_test_user():
    """Sends a login request to the backend and handles the response."""
    
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    print(f"Attempting to log in as: {TEST_USER_EMAIL}")
    print(f"Target URL: {BACKEND_URL}")

    try:
        response = requests.post(BACKEND_URL, json=login_data)
        
        if response.status_code >= 400 and response.status_code != 401:
            response.raise_for_status()

        result = response.json()
        
        if response.status_code == 200 and 'token' in result:
            print("\n--- Login Successful! ---")
            print(f"Message: {result.get('message')}")
            print(f"Received JWT Token (first 30 characters): {result.get('token')[:30]}...")
            print("\nThis token will be crucial for accessing protected data endpoints in the future.")
        else:
            print(f"\n--- Login Failed (HTTP {response.status_code}) ---")
            print(f"Response: {result.get('message')}")

    except requests.exceptions.RequestException as e:
        print(f"\n--- ERROR: Could not connect or post data ---")
        print("Details: Ensure 'backend.py' is running and accessible at http://127.0.0.1:5000")
        print(f"Error: {e}")

if __name__ == '__main__':
    login_test_user()