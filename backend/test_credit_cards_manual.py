"""
Manual test script for credit card endpoints.
This script tests the credit card management functionality.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def test_credit_cards():
    print("=" * 60)
    print("Testing Credit Card Management Endpoints")
    print("=" * 60)
    
    # Step 1: Register a user
    print("\n1. Registering a new user...")
    register_data = {
        "email": "test_credit_cards@example.com",
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
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server. Make sure Flask is running on port 5000")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Create a shared account
    print("\n2. Creating shared account...")
    response = requests.post(f"{BASE_URL}/account/invite", 
                            json={"invitee_email": "spouse@example.com"},
                            headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"✓ Shared account created")
    else:
        print(f"Note: {response.text}")
    
    # Step 3: Create a credit card
    print("\n3. Creating a credit card...")
    card_data = {
        "name": "Visa Gold Card",
        "credit_limit": 5000.00,
        "current_balance": 1250.50
    }
    response = requests.post(f"{BASE_URL}/credit-cards", json=card_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        card = response.json().get('credit_card')
        card_id = card.get('id')
        print(f"✓ Credit card created successfully")
        print(f"  ID: {card_id}")
        print(f"  Name: {card.get('name')}")
        print(f"  Credit Limit: ${card.get('credit_limit')}")
        print(f"  Current Balance: ${card.get('current_balance')}")
        print(f"  Available Credit: ${card.get('available_credit')}")
    else:
        print(f"✗ Failed to create credit card: {response.text}")
        return
    
    # Step 4: Get all credit cards
    print("\n4. Getting all credit cards...")
    response = requests.get(f"{BASE_URL}/credit-cards", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        cards = response.json().get('credit_cards', [])
        print(f"✓ Retrieved {len(cards)} credit card(s)")
        for card in cards:
            print(f"  - {card.get('name')}: ${card.get('current_balance')} / ${card.get('credit_limit')}")
    else:
        print(f"✗ Failed to get credit cards: {response.text}")
    
    # Step 5: Update credit card
    print("\n5. Updating credit card...")
    update_data = {
        "name": "Visa Platinum Card",
        "credit_limit": 7500.00
    }
    response = requests.put(f"{BASE_URL}/credit-cards/{card_id}", json=update_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        card = response.json().get('credit_card')
        print(f"✓ Credit card updated successfully")
        print(f"  Name: {card.get('name')}")
        print(f"  Credit Limit: ${card.get('credit_limit')}")
        print(f"  Available Credit: ${card.get('available_credit')}")
    else:
        print(f"✗ Failed to update credit card: {response.text}")
    
    # Step 6: Record a payment transaction
    print("\n6. Recording a payment transaction...")
    payment_data = {
        "amount": 500.00,
        "type": "payment",
        "date": datetime.now().strftime('%Y-%m-%d'),
        "description": "Monthly payment"
    }
    response = requests.post(f"{BASE_URL}/credit-cards/{card_id}/transactions", 
                            json=payment_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        transaction = response.json().get('transaction')
        card = response.json().get('credit_card')
        print(f"✓ Payment transaction recorded successfully")
        print(f"  Amount: ${transaction.get('amount')}")
        print(f"  Type: {transaction.get('type')}")
        print(f"  New Balance: ${card.get('current_balance')}")
        print(f"  Available Credit: ${card.get('available_credit')}")
    else:
        print(f"✗ Failed to record payment: {response.text}")
    
    # Step 7: Record a charge transaction
    print("\n7. Recording a charge transaction...")
    charge_data = {
        "amount": 150.75,
        "type": "charge",
        "date": datetime.now().strftime('%Y-%m-%d'),
        "description": "Online purchase"
    }
    response = requests.post(f"{BASE_URL}/credit-cards/{card_id}/transactions", 
                            json=charge_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        transaction = response.json().get('transaction')
        card = response.json().get('credit_card')
        print(f"✓ Charge transaction recorded successfully")
        print(f"  Amount: ${transaction.get('amount')}")
        print(f"  Type: {transaction.get('type')}")
        print(f"  New Balance: ${card.get('current_balance')}")
        print(f"  Available Credit: ${card.get('available_credit')}")
    else:
        print(f"✗ Failed to record charge: {response.text}")
    
    print("\n" + "=" * 60)
    print("Credit Card Management Tests Completed")
    print("=" * 60)

if __name__ == "__main__":
    test_credit_cards()
