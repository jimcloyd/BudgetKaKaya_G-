"""
Manual test script for dashboard endpoint
Run this after starting the Flask server to test the dashboard functionality
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def print_response(response):
    """Pretty print response"""
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 80)

def test_dashboard():
    """Test dashboard endpoint"""
    print("\n=== Testing Dashboard Endpoint ===\n")
    
    # First, register and login to get a token
    print("1. Registering test user...")
    register_data = {
        "email": f"dashboard_test_{datetime.now().timestamp()}@example.com",
        "password": "testpass123",
        "name": "Dashboard Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response(response)
    
    if response.status_code != 201:
        print("Registration failed!")
        return
    
    # Login
    print("2. Logging in...")
    login_data = {
        "email": register_data["email"],
        "password": register_data["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    if response.status_code != 200:
        print("Login failed!")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create shared account by inviting self (simplified test)
    # In real scenario, we'd need two users
    print("3. Creating shared account...")
    # For testing, we'll just add some test data
    
    # Add a category
    print("4. Creating test category...")
    category_data = {"name": "Test Category", "is_custom": True}
    response = requests.post(f"{BASE_URL}/categories", json=category_data, headers=headers)
    print_response(response)
    
    if response.status_code == 201:
        category_id = response.json()["category"]["id"]
        
        # Add some expenses
        print("5. Creating test expenses...")
        today = datetime.now().date()
        
        # Current month expense
        expense_data = {
            "amount": 150.50,
            "category_id": category_id,
            "date": today.isoformat(),
            "description": "Test expense 1"
        }
        response = requests.post(f"{BASE_URL}/expenses", json=expense_data, headers=headers)
        print_response(response)
        
        # Another current month expense
        expense_data = {
            "amount": 75.25,
            "category_id": category_id,
            "date": (today - timedelta(days=5)).isoformat(),
            "description": "Test expense 2"
        }
        response = requests.post(f"{BASE_URL}/expenses", json=expense_data, headers=headers)
        print_response(response)
        
        # Previous month expense for comparison
        last_month = today.replace(day=1) - timedelta(days=1)
        expense_data = {
            "amount": 200.00,
            "category_id": category_id,
            "date": last_month.isoformat(),
            "description": "Last month expense"
        }
        response = requests.post(f"{BASE_URL}/expenses", json=expense_data, headers=headers)
        print_response(response)
        
        # Add budget limit
        print("6. Creating budget limit...")
        budget_data = {
            "category_id": category_id,
            "amount": 300.00,
            "period": "monthly"
        }
        response = requests.post(f"{BASE_URL}/budgets", json=budget_data, headers=headers)
        print_response(response)
        
        # Add monthly income
        print("7. Setting monthly income...")
        income_data = {
            "month": today.month,
            "year": today.year,
            "amount": 5000.00
        }
        response = requests.post(f"{BASE_URL}/income", json=income_data, headers=headers)
        print_response(response)
        
        # Add an installment
        print("8. Creating installment...")
        installment_data = {
            "total_amount": 1200.00,
            "number_of_payments": 12,
            "start_date": today.replace(day=1).isoformat(),
            "description": "Test installment"
        }
        response = requests.post(f"{BASE_URL}/installments", json=installment_data, headers=headers)
        print_response(response)
    
    # Now test the dashboard endpoint
    print("\n9. Testing Dashboard Endpoint...")
    response = requests.get(f"{BASE_URL}/dashboard", headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print("\n=== Dashboard Summary ===")
        print(f"Total Expenses (Current Month): ${data.get('total_expenses', 0):.2f}")
        print(f"Monthly Income: ${data.get('monthly_income', 0):.2f}")
        print(f"Net Income: ${data.get('net_income', 0):.2f}")
        print(f"\nBudget Status Items: {len(data.get('budget_status', []))}")
        print(f"Recent Expenses: {len(data.get('recent_expenses', []))}")
        print(f"Upcoming Installments: {len(data.get('upcoming_installments', []))}")
        print(f"\nSpending Comparison:")
        comparison = data.get('spending_comparison', {})
        print(f"  Current Month: ${comparison.get('current_month', 0):.2f}")
        print(f"  Previous Month: ${comparison.get('previous_month', 0):.2f}")
        print(f"  Change: ${comparison.get('change_amount', 0):.2f} ({comparison.get('change_percentage', 0):.2f}%)")
        print("\n✓ Dashboard endpoint working correctly!")
    else:
        print("\n✗ Dashboard endpoint failed!")

if __name__ == "__main__":
    try:
        test_dashboard()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n✗ Error: {e}")
