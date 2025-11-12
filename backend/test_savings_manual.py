"""
Manual test script for savings goals endpoints
Run this after starting the Flask server to test the savings goals functionality
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

# Test credentials
TEST_USER = {
    "email": "test_savings@example.com",
    "password": "testpass123",
    "name": "Test Savings User"
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

def test_savings_goals():
    """Test savings goals endpoints"""
    
    # Step 1: Register user
    print("\n1. Registering test user...")
    response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
    print_response(response, "REGISTER USER")
    
    if response.status_code != 201:
        print("Registration failed. User might already exist. Trying to login...")
    
    # Step 2: Login
    print("\n2. Logging in...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    print_response(response, "LOGIN")
    
    if response.status_code != 200:
        print("Login failed. Exiting...")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Create a shared account (invite self)
    print("\n3. Creating shared account...")
    response = requests.post(f"{BASE_URL}/account/invite", 
                            json={"invitee_email": TEST_USER["email"]},
                            headers=headers)
    print_response(response, "CREATE SHARED ACCOUNT")
    
    # Step 4: Create savings goal without target date
    print("\n4. Creating savings goal (Emergency Fund)...")
    goal_data = {
        "name": "Emergency Fund",
        "target_amount": 10000.00
    }
    response = requests.post(f"{BASE_URL}/savings-goals", json=goal_data, headers=headers)
    print_response(response, "CREATE SAVINGS GOAL (No Target Date)")
    
    if response.status_code != 201:
        print("Failed to create savings goal. Exiting...")
        return
    
    goal1_id = response.json()["savings_goal"]["id"]
    
    # Step 5: Create savings goal with target date
    print("\n5. Creating savings goal with target date (Vacation Fund)...")
    target_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    goal_data = {
        "name": "Vacation Fund",
        "target_amount": 5000.00,
        "target_date": target_date
    }
    response = requests.post(f"{BASE_URL}/savings-goals", json=goal_data, headers=headers)
    print_response(response, "CREATE SAVINGS GOAL (With Target Date)")
    
    if response.status_code != 201:
        print("Failed to create second savings goal.")
        goal2_id = None
    else:
        goal2_id = response.json()["savings_goal"]["id"]
    
    # Step 6: Get all savings goals
    print("\n6. Getting all savings goals...")
    response = requests.get(f"{BASE_URL}/savings-goals", headers=headers)
    print_response(response, "GET ALL SAVINGS GOALS")
    
    # Step 7: Add contribution to first goal
    print("\n7. Adding contribution to Emergency Fund...")
    contribution_data = {
        "amount": 1500.00,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    response = requests.post(f"{BASE_URL}/savings-goals/{goal1_id}/contributions", 
                            json=contribution_data, headers=headers)
    print_response(response, "ADD CONTRIBUTION")
    
    # Step 8: Add another contribution
    print("\n8. Adding another contribution to Emergency Fund...")
    contribution_data = {
        "amount": 2500.00,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    response = requests.post(f"{BASE_URL}/savings-goals/{goal1_id}/contributions", 
                            json=contribution_data, headers=headers)
    print_response(response, "ADD SECOND CONTRIBUTION")
    
    # Step 9: Add contribution to second goal (if exists)
    if goal2_id:
        print("\n9. Adding contribution to Vacation Fund...")
        contribution_data = {
            "amount": 500.00,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        response = requests.post(f"{BASE_URL}/savings-goals/{goal2_id}/contributions", 
                                json=contribution_data, headers=headers)
        print_response(response, "ADD CONTRIBUTION TO VACATION FUND")
    
    # Step 10: Update savings goal
    print("\n10. Updating Emergency Fund target amount...")
    update_data = {
        "target_amount": 15000.00
    }
    response = requests.put(f"{BASE_URL}/savings-goals/{goal1_id}", 
                           json=update_data, headers=headers)
    print_response(response, "UPDATE SAVINGS GOAL")
    
    # Step 11: Get all savings goals again to see updated values
    print("\n11. Getting all savings goals (after updates)...")
    response = requests.get(f"{BASE_URL}/savings-goals", headers=headers)
    print_response(response, "GET ALL SAVINGS GOALS (FINAL)")
    
    # Verify calculations
    if response.status_code == 200:
        goals = response.json()["savings_goals"]
        print("\n" + "="*60)
        print("VERIFICATION OF CALCULATIONS")
        print("="*60)
        for goal in goals:
            print(f"\nGoal: {goal['name']}")
            print(f"  Target: ${goal['target_amount']}")
            print(f"  Current: ${goal['current_balance']}")
            print(f"  Percentage: {goal['percentage_completed']}%")
            print(f"  Remaining: ${goal['remaining_amount']}")
            if goal['suggested_monthly_contribution']:
                print(f"  Suggested Monthly: ${goal['suggested_monthly_contribution']}")
            else:
                print(f"  Suggested Monthly: N/A (no target date)")
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60)

if __name__ == "__main__":
    print("Starting Savings Goals Manual Tests...")
    print("Make sure the Flask server is running on http://localhost:5000")
    input("Press Enter to continue...")
    
    try:
        test_savings_goals()
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the server.")
        print("Please make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
