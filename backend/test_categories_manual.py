"""
Manual test script for category endpoints.
This script tests the category management functionality.
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_categories():
    print("=" * 60)
    print("Testing Category Management Endpoints")
    print("=" * 60)
    
    # Step 1: Register a user
    print("\n1. Registering a new user...")
    register_data = {
        "email": "test_categories@example.com",
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
    
    # Step 2: Try to get categories (should fail - no shared account yet)
    print("\n2. Getting categories (should fail - no shared account)...")
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 403:
            print(f"✓ Correctly rejected: {response.json().get('message')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 3: Create a shared account by inviting a spouse
    print("\n3. Creating shared account (inviting spouse)...")
    invite_data = {
        "email": "spouse_categories@example.com"
    }
    
    # First register the spouse
    print("   Registering spouse...")
    spouse_register_data = {
        "email": "spouse_categories@example.com",
        "password": "spousepass123",
        "name": "Spouse User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=spouse_register_data)
        if response.status_code in [201, 409]:
            print(f"   ✓ Spouse account ready")
        else:
            print(f"   ✗ Spouse registration failed: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Now send invitation
    try:
        response = requests.post(f"{BASE_URL}/account/invite", json=invite_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print(f"✓ Invitation sent successfully")
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 4: Get categories (should now work and show default categories)
    print("\n4. Getting categories (should show default categories)...")
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            print(f"✓ Retrieved {len(categories)} categories:")
            for cat in categories:
                print(f"  - {cat['name']} (custom: {cat['is_custom']})")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 5: Create a custom category
    print("\n5. Creating a custom category...")
    custom_category_data = {
        "name": "Dining Out"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/categories", json=custom_category_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Custom category created:")
            print(f"  {json.dumps(data['category'], indent=2)}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 6: Try to create duplicate category (should fail)
    print("\n6. Creating duplicate category (should fail)...")
    duplicate_data = {
        "name": "groceries"  # Already exists as default
    }
    
    try:
        response = requests.post(f"{BASE_URL}/categories", json=duplicate_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 409:
            print(f"✓ Correctly rejected duplicate: {response.json().get('message')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 7: Get all categories again (should include custom category)
    print("\n7. Getting all categories (should include custom category)...")
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            print(f"✓ Retrieved {len(categories)} categories:")
            for cat in categories:
                custom_marker = " [CUSTOM]" if cat['is_custom'] else ""
                print(f"  - {cat['name']}{custom_marker}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 8: Try to create category with empty name (should fail)
    print("\n8. Creating category with empty name (should fail)...")
    empty_name_data = {
        "name": "   "
    }
    
    try:
        response = requests.post(f"{BASE_URL}/categories", json=empty_name_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print(f"✓ Correctly rejected empty name: {response.json().get('message')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Category Management Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Press Enter to start tests or Ctrl+C to cancel...")
    input()
    test_categories()
