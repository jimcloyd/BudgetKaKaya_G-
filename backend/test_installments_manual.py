"""
Manual test script for installment endpoints
Run this after starting the Flask server to test the installment functionality
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

# Test credentials (update these with actual test user credentials)
TEST_USER = {
    "email": "test@example.com",
    "password": "testpassword123"
}

def login():
    """Login and get JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login", json=TEST_USER)
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("✓ Login successful")
        return token
    else:
        print(f"✗ Login failed: {response.json()}")
        return None

def test_create_installment(token):
    """Test creating a new installment"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Calculate start date (first day of current month)
    start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
    
    installment_data = {
        "total_amount": 12000.00,
        "number_of_payments": 12,
        "start_date": start_date,
        "description": "New laptop purchase"
    }
    
    response = requests.post(f"{BASE_URL}/installments", json=installment_data, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        print("✓ Installment created successfully")
        print(f"  ID: {data['installment']['id']}")
        print(f"  Total Amount: ${data['installment']['total_amount']}")
        print(f"  Monthly Payment: ${data['installment']['monthly_payment']}")
        print(f"  Remaining Balance: ${data['installment']['remaining_balance']}")
        print(f"  Next Payment Date: {data['installment']['next_payment_date']}")
        return data['installment']['id']
    else:
        print(f"✗ Failed to create installment: {response.json()}")
        return None

def test_get_installments(token):
    """Test getting all installments"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/installments", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Retrieved {len(data['installments'])} installments")
        for inst in data['installments']:
            print(f"  - {inst['description']}: ${inst['monthly_payment']}/month, {inst['paid_payments']}/{inst['number_of_payments']} paid")
        return data['installments']
    else:
        print(f"✗ Failed to get installments: {response.json()}")
        return []

def test_mark_payment(token, installment_id):
    """Test marking a payment as completed"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/installments/{installment_id}/pay", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Payment marked as completed")
        print(f"  Paid Payments: {data['installment']['paid_payments']}/{data['installment']['number_of_payments']}")
        print(f"  Remaining Balance: ${data['installment']['remaining_balance']}")
        print(f"  Next Payment Date: {data['installment']['next_payment_date']}")
        return True
    else:
        print(f"✗ Failed to mark payment: {response.json()}")
        return False

def test_validation_errors(token):
    """Test validation error handling"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nTesting validation errors:")
    
    # Test missing required fields
    response = requests.post(f"{BASE_URL}/installments", json={}, headers=headers)
    if response.status_code == 422:
        print("✓ Missing fields validation works")
    else:
        print(f"✗ Missing fields validation failed: {response.status_code}")
    
    # Test invalid amount
    response = requests.post(f"{BASE_URL}/installments", json={
        "total_amount": -100,
        "number_of_payments": 12,
        "start_date": "2024-01-01",
        "description": "Test"
    }, headers=headers)
    if response.status_code == 422:
        print("✓ Negative amount validation works")
    else:
        print(f"✗ Negative amount validation failed: {response.status_code}")
    
    # Test invalid number of payments
    response = requests.post(f"{BASE_URL}/installments", json={
        "total_amount": 1000,
        "number_of_payments": 0,
        "start_date": "2024-01-01",
        "description": "Test"
    }, headers=headers)
    if response.status_code == 422:
        print("✓ Invalid number of payments validation works")
    else:
        print(f"✗ Invalid number of payments validation failed: {response.status_code}")
    
    # Test invalid date format
    response = requests.post(f"{BASE_URL}/installments", json={
        "total_amount": 1000,
        "number_of_payments": 12,
        "start_date": "invalid-date",
        "description": "Test"
    }, headers=headers)
    if response.status_code == 422:
        print("✓ Invalid date format validation works")
    else:
        print(f"✗ Invalid date format validation failed: {response.status_code}")

def main():
    print("=" * 60)
    print("INSTALLMENT ENDPOINTS MANUAL TEST")
    print("=" * 60)
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("and you have a test user with shared account access.\n")
    
    # Login
    token = login()
    if not token:
        print("\nTests aborted - login failed")
        return
    
    print("\n" + "-" * 60)
    print("TEST 1: Create Installment")
    print("-" * 60)
    installment_id = test_create_installment(token)
    
    print("\n" + "-" * 60)
    print("TEST 2: Get All Installments")
    print("-" * 60)
    test_get_installments(token)
    
    if installment_id:
        print("\n" + "-" * 60)
        print("TEST 3: Mark Payment as Completed")
        print("-" * 60)
        test_mark_payment(token, installment_id)
        
        print("\n" + "-" * 60)
        print("TEST 4: Mark Another Payment")
        print("-" * 60)
        test_mark_payment(token, installment_id)
        
        print("\n" + "-" * 60)
        print("TEST 5: View Updated Installments")
        print("-" * 60)
        test_get_installments(token)
    
    print("\n" + "-" * 60)
    print("TEST 6: Validation Errors")
    print("-" * 60)
    test_validation_errors(token)
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
