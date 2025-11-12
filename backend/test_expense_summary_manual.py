"""
Manual test script for expense summary endpoint.
This script tests the expense summary functionality.
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def test_expense_summary():
    print("=" * 60)
    print("Testing Expense Summary Endpoint")
    print("=" * 60)
    
    # Step 1: Register and login
    print("\n1. Setting up test user...")
    register_data = {
        "email": "test_summary@example.com",
        "password": "testpass123",
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            token = response.json().get('access_token')
            print(f"✓ User registered successfully")
        elif response.status_code == 409:
            # Login if user exists
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": register_data["email"],
                "password": register_data["password"]
            })
            token = response.json().get('access_token')
            print(f"✓ Logged in successfully")
        else:
            print(f"✗ Setup failed: {response.text}")
            return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Create shared account
    print("\n2. Setting up shared account...")
    spouse_data = {
        "email": "spouse_summary@example.com",
        "password": "spousepass123",
        "name": "Spouse User"
    }
    
    try:
        requests.post(f"{BASE_URL}/auth/register", json=spouse_data)
        response = requests.post(f"{BASE_URL}/account/invite", 
                                json={"email": spouse_data["email"]}, 
                                headers=headers)
        if response.status_code == 201:
            print(f"✓ Shared account created")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 3: Get categories
    print("\n3. Getting categories...")
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=headers)
        if response.status_code == 200:
            categories = response.json().get('categories', [])
            print(f"✓ Retrieved {len(categories)} categories")
            category_map = {cat['name']: cat['id'] for cat in categories}
        else:
            print(f"✗ Failed to get categories: {response.text}")
            return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 4: Create test expenses
    print("\n4. Creating test expenses...")
    today = datetime.now().date()
    test_expenses = [
        {"amount": 150.50, "category": "groceries", "description": "Weekly groceries"},
        {"amount": 200.00, "category": "groceries", "description": "More groceries"},
        {"amount": 75.25, "category": "utilities", "description": "Electric bill"},
        {"amount": 50.00, "category": "transportation", "description": "Gas"},
        {"amount": 100.00, "category": "entertainment", "description": "Movie tickets"},
        {"amount": 30.00, "category": "entertainment", "description": "Streaming"},
    ]
    
    created_count = 0
    for expense_data in test_expenses:
        try:
            expense = {
                "amount": expense_data["amount"],
                "category_id": category_map.get(expense_data["category"]),
                "date": today.isoformat(),
                "description": expense_data["description"]
            }
            response = requests.post(f"{BASE_URL}/expenses", json=expense, headers=headers)
            if response.status_code == 201:
                created_count += 1
        except Exception as e:
            print(f"  ✗ Error creating expense: {e}")
    
    print(f"✓ Created {created_count} test expenses")
    
    # Step 5: Get expense summary (no filters)
    print("\n5. Getting expense summary (all expenses)...")
    try:
        response = requests.get(f"{BASE_URL}/expenses/summary", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            summary = data.get('summary', [])
            grand_total = data.get('grand_total', 0)
            
            print(f"✓ Retrieved summary for {len(summary)} categories")
            print(f"\n  Grand Total: ${grand_total:.2f}\n")
            
            for item in summary:
                print(f"  {item['category_name']}:")
                print(f"    Total: ${item['total_amount']:.2f}")
                print(f"    Percentage: {item['percentage']:.1f}%")
                print(f"    Expenses: {item['expense_count']}")
                print()
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 6: Get expense summary with date filter
    print("\n6. Getting expense summary with date range...")
    start_date = (today - timedelta(days=7)).isoformat()
    end_date = today.isoformat()
    
    try:
        response = requests.get(
            f"{BASE_URL}/expenses/summary?start_date={start_date}&end_date={end_date}", 
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            summary = data.get('summary', [])
            print(f"✓ Retrieved summary for date range: {start_date} to {end_date}")
            print(f"  Categories: {len(summary)}")
            print(f"  Grand Total: ${data.get('grand_total', 0):.2f}")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 7: Test with invalid date format
    print("\n7. Testing with invalid date format (should fail)...")
    try:
        response = requests.get(
            f"{BASE_URL}/expenses/summary?start_date=invalid-date", 
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print(f"✓ Correctly rejected invalid date: {response.json().get('message')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Expense Summary Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Press Enter to start tests or Ctrl+C to cancel...")
    input()
    test_expense_summary()
