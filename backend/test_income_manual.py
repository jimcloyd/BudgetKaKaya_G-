"""
Manual test script for income endpoints
Run this after starting the Flask server to test the income API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

# Test credentials
TEST_USER = {
    "email": "test_income@example.com",
    "password": "testpass123",
    "name": "Income Test User"
}

def print_response(response, title):
    """Helper to print formatted response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_income_endpoints():
    """Test all income endpoints"""
    
    # Step 1: Register and login
    print("\n" + "="*60)
    print("STEP 1: Register and Login")
    print("="*60)
    
    # Register
    response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
    print_response(response, "Register User")
    
    # Login
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    print_response(response, "Login")
    
    if response.status_code != 200:
        print("\n❌ Login failed. Cannot proceed with tests.")
        return
    
    token = response.json().get('access_token')
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Create shared account (invite self)
    print("\n" + "="*60)
    print("STEP 2: Create Shared Account")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/account/invite", 
                            json={"invitee_email": TEST_USER["email"]},
                            headers=headers)
    print_response(response, "Send Invitation")
    
    if response.status_code == 201:
        invitation_id = response.json().get('invitation', {}).get('id')
        
        # Accept invitation
        response = requests.post(f"{BASE_URL}/account/accept-invite",
                                json={"invitation_id": invitation_id},
                                headers=headers)
        print_response(response, "Accept Invitation")
    
    # Step 3: Test POST /api/income - Create monthly income
    print("\n" + "="*60)
    print("STEP 3: Create Monthly Income")
    print("="*60)
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    income_data = {
        "month": current_month,
        "year": current_year,
        "amount": 5000.00
    }
    
    response = requests.post(f"{BASE_URL}/income", json=income_data, headers=headers)
    print_response(response, "Create Monthly Income")
    
    income_id = None
    if response.status_code == 201:
        income_id = response.json().get('monthly_income', {}).get('id')
        print(f"\n✅ Monthly income created with ID: {income_id}")
    
    # Step 4: Test duplicate creation (should fail with 409)
    print("\n" + "="*60)
    print("STEP 4: Test Duplicate Creation (Should Fail)")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/income", json=income_data, headers=headers)
    print_response(response, "Attempt Duplicate Creation")
    
    if response.status_code == 409:
        print("\n✅ Correctly rejected duplicate income entry")
    
    # Step 5: Test GET /api/income - Get all incomes
    print("\n" + "="*60)
    print("STEP 5: Get All Monthly Incomes")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/income", headers=headers)
    print_response(response, "Get All Monthly Incomes")
    
    # Step 6: Test GET with filters
    print("\n" + "="*60)
    print("STEP 6: Get Monthly Incomes with Filters")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/income?month={current_month}&year={current_year}", 
                           headers=headers)
    print_response(response, f"Get Income for {current_month}/{current_year}")
    
    # Step 7: Create income for different month
    print("\n" + "="*60)
    print("STEP 7: Create Income for Different Month")
    print("="*60)
    
    next_month = current_month + 1 if current_month < 12 else 1
    next_year = current_year if current_month < 12 else current_year + 1
    
    income_data_2 = {
        "month": next_month,
        "year": next_year,
        "amount": 5500.00
    }
    
    response = requests.post(f"{BASE_URL}/income", json=income_data_2, headers=headers)
    print_response(response, f"Create Income for {next_month}/{next_year}")
    
    income_id_2 = None
    if response.status_code == 201:
        income_id_2 = response.json().get('monthly_income', {}).get('id')
    
    # Step 8: Test PUT /api/income/:id - Update income
    print("\n" + "="*60)
    print("STEP 8: Update Monthly Income")
    print("="*60)
    
    if income_id:
        update_data = {
            "amount": 5250.50
        }
        
        response = requests.put(f"{BASE_URL}/income/{income_id}", 
                               json=update_data, 
                               headers=headers)
        print_response(response, "Update Monthly Income Amount")
        
        if response.status_code == 200:
            print("\n✅ Monthly income updated successfully")
    
    # Step 9: Test validation errors
    print("\n" + "="*60)
    print("STEP 9: Test Validation Errors")
    print("="*60)
    
    # Invalid month
    invalid_data = {
        "month": 13,
        "year": current_year,
        "amount": 5000.00
    }
    response = requests.post(f"{BASE_URL}/income", json=invalid_data, headers=headers)
    print_response(response, "Invalid Month (13)")
    
    # Invalid amount (negative)
    invalid_data = {
        "month": current_month,
        "year": current_year - 1,
        "amount": -1000.00
    }
    response = requests.post(f"{BASE_URL}/income", json=invalid_data, headers=headers)
    print_response(response, "Invalid Amount (Negative)")
    
    # Missing required fields
    invalid_data = {
        "month": current_month
    }
    response = requests.post(f"{BASE_URL}/income", json=invalid_data, headers=headers)
    print_response(response, "Missing Required Fields")
    
    # Step 10: Get all incomes to verify
    print("\n" + "="*60)
    print("STEP 10: Final Verification - Get All Incomes")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/income", headers=headers)
    print_response(response, "Get All Monthly Incomes")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("INCOME ENDPOINTS MANUAL TEST")
    print("="*60)
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Press Enter to start tests or Ctrl+C to cancel...")
    input()
    
    try:
        test_income_endpoints()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server. Make sure Flask is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
