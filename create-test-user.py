#!/usr/bin/env python3
"""
Script to create a test user directly in the database
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from app.models import User
import bcrypt

# User details
EMAIL = 'jimcloyd@gmail.com'
PASSWORD = 'jimcloyd'
NAME = 'Jim Cloyd'

def create_user():
    try:
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            # Check if user already exists
            existing = User.query.filter_by(email=EMAIL).first()
            
            if existing:
                print(f"❌ User {EMAIL} already exists!")
                print(f"   You can login with:")
                print(f"   Email: {EMAIL}")
                print(f"   Password: {PASSWORD}")
                return True
            
            # Hash the password
            password_hash = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Create new user
            new_user = User(
                email=EMAIL,
                password=password_hash,
                name=NAME
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            print(f"✅ User created successfully!")
            print(f"   Email: {EMAIL}")
            print(f"   Password: {PASSWORD}")
            print(f"   Name: {NAME}")
            print(f"   ID: {new_user.id}")
            return True
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_user()
