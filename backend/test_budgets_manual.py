"""
Manual test script for budget endpoints.
This script tests the budget management functionality.
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def test_budgets():
    print("=" * 60)
    print("Testing Budget Management Endpoints")
    print("=" * 60)
    
    # Step 1: Register a user
    print("\n1. Registering a new user...")
    register_data = {
        "email": "test_budgets@example.com",
        "password": "testpass123",
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            token = data.get('access_token')
            print(f"✓ User registered successfully")
            print(f"  Token: {token[:20]}...")
        elif response.status_code == 409:
            # User already exists, try to login
            print("User already exists, logging in...")
            login_data = {
                "email": register_data["email"],
                "password": register_data["password"]
            }
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                print(f"✓ Logged in successfully")
            else:
                print(f"✗ Login failed: {response.text}")
                return
        else:
            print(f"✗ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Create a shared account by inviting a spouse
    print("\n2. Creating shared account (inviting spouse)...")
    invite_data = {
        "email": "spouse_budgets@example.com"
    }
    
    # First register the spouse
    print("   Registering spouse...")
    spouse_register_data = {
        "email": "spouse_budgets@example.com",
        "password": "spousepass123",
        "name": "Spouse User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=spouse_register_data)
        if response.status_code in [201, 409]:
            print(f"   ✓ Spouse account ready")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Now send invitation
    try:
        response = requests.post(f"{BASE_URL}/account/invite", json=invite_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print(f"✓ Invitation sent successfully")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 3: Get categories to use for budget limits
    print("\n3. Getting categories...")
    category_id = None
    category_name = None
    
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            if categories:
                category_id = categories[0]['id']
                category_name = categories[0]['name']
                print(f"✓ Using category: {category_name} (ID: {category_id})")
        else:
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 4: Get budgets (should be empty initially)
    print("\n4. Getting budgets (should be empty)...")
    try:
        response = requests.get(f"{BASE_URL}/budgets", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            budgets = data.get('budgets', [])
            print(f"✓ Retrieved {len(budgets)} budgets")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 5: Create a monthly budget limit
    print("\n5. Creating a monthly budget limit...")
    budget_data = {
        "category_id": category_id,
        "amount": 500.00,
        "period": "monthly"
    }
    
    budget_id = None
    try:
        response = requests.post(f"{BASE_URL}/budgets", json=budget_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            budget_id = data['budget']['id']
            print(f"✓ Budget limit created:")
            print(f"  {json.dumps(data['budget'], indent=2)}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 6: Create a weekly budget limit for another category
    print("\n6. Creating a weekly budget limit...")
    # Get another category
    second_category_id = None
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=headers)
        if response.status_code == 200:
            categories = response.json().get('categories', [])
            if len(categories) > 1:
                second_category_id = categories[1]['id']
                second_category_name = categories[1]['name']
    except Exception as e:
        pass
    
    if second_category_id:
        weekly_budget_data = {
            "category_id": second_category_id,
            "amount": 100.00,
            "period": "weekly"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/budgets", json=weekly_budget_data, headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                print(f"✓ Weekly budget limit created for {second_category_name}")
            else:
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Step 7: Try to create duplicate budget (should fail)
    print("\n7. Creating duplicate budget (should fail)...")
    try:
        response = requests.post(f"{BASE_URL}/budgets", json=budget_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 409:
            print(f"✓ Correctly rejected duplicate: {response.json().get('message')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 8: Try to create budget with invalid period (should fail)
    print("\n8. Creating budget with invalid period (should fail)...")
    invalid_period_data = {
        "category_id": category_id,
        "amount": 300.00,
        "period": "yearly"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/budgets", json=invalid_period_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print(f"✓ Correctly rejected invalid period: {response.json().get('message')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 9: Update budget limit
    print("\n9. Updating budget limit...")
    if budget_id:
        update_data = {
            "amount": 600.00
        }
        
        try:
            response = requests.put(f"{BASE_URL}/budgets/{budget_id}", json=update_data, headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Budget limit updated:")
                print(f"  New amount: ${data['budget']['amount']}")
            else:
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Step 10: Get all budgets
    print("\n10. Getting all budgets...")
    try:
        response = requests.get(f"{BASE_URL}/budgets", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            budgets = data.get('budgets', [])
            print(f"✓ Retrieved {len(budgets)} budgets:")
            for budget in budgets:
                print(f"  - {budget['category_name']}: ${budget['amount']} ({budget['period']})")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 11: Create some expenses to test budget status
    print("\n11. Creating expenses to test budget status...")
    today = datetime.now().strftime('%Y-%m-%d')
    
    expense_data = {
        "category_id": category_id,
        "amount": 250.00,
        "date": today,
        "description": "Test expense for budget tracking"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/expenses", json=expense_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print(f"✓ Expense created: ${expense_data['amount']}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Create another expense to reach 80% threshold
    expense_data2 = {
        "category_id": category_id,
        "amount": 230.00,
        "date": today,
        "description": "Second test expense"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/expenses", json=expense_data2, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print(f"✓ Second expense created: ${expense_data2['amount']}")
            print(f"  Total spent: ${expense_data['amount'] + expense_data2['amount']} / $600.00")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 12: Get budget status (should show warning)
    print("\n12. Getting budget status (should show warning at 80%)...")
    try:
        response = requests.get(f"{BASE_URL}/budgets/status", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            budget_status = data.get('budget_status', [])
            print(f"✓ Budget status retrieved:")
            for status in budget_status:
                print(f"\n  Category: {status['category_name']}")
                print(f"  Budget: ${status['budget_amount']} ({status['period']})")
                print(f"  Spent: ${status['spent']}")
                print(f"  Remaining: ${status['remaining']}")
                print(f"  Percentage: {status['percentage']}%")
                print(f"  Status: {status['status']}")
                print(f"  Period: {status['period_start']} to {status['period_end']}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 13: Create expense to exceed budget
    print("\n13. Creating expense to exceed budget...")
    expense_data3 = {
        "category_id": category_id,
        "amount": 150.00,
        "date": today,
        "description": "Third test expense to exceed budget"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/expenses", json=expense_data3, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print(f"✓ Third expense created: ${expense_data3['amount']}")
            total = expense_data['amount'] + expense_data2['amount'] + expense_data3['amount']
            print(f"  Total spent: ${total} / $600.00 (exceeded!)")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 14: Get budget status again (should show exceeded)
    print("\n14. Getting budget status (should show exceeded)...")
    try:
        response = requests.get(f"{BASE_URL}/budgets/status", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            budget_status = data.get('budget_status', [])
            print(f"✓ Budget status retrieved:")
            for status in budget_status:
                if status['category_id'] == category_id:
                    print(f"\n  Category: {status['category_name']}")
                    print(f"  Budget: ${status['budget_amount']} ({status['period']})")
                    print(f"  Spent: ${status['spent']}")
                    print(f"  Remaining: ${status['remaining']}")
                    print(f"  Percentage: {status['percentage']}%")
                    print(f"  Status: {status['status']} ⚠️")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Budget Management Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Press Enter to start tests or Ctrl+C to cancel...")
    input()
    test_budgets()
