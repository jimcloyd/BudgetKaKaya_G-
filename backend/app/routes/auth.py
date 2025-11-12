from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
import bcrypt

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user with email, password, and name"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Validation Error', 'message': 'Email, password, and name are required'}), 422
    
    email = data.get('email').strip().lower()
    password = data.get('password')
    name = data.get('name').strip()
    
    # Validate password length (min 8 characters)
    if len(password) < 8:
        return jsonify({'error': 'Validation Error', 'message': 'Password must be at least 8 characters long'}), 422
    
    # Note: Password confirmation validation is handled on frontend
    # Backend accepts single password field for simplicity
    
    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Conflict', 'message': 'Email already registered'}), 409
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create new user
    new_user = User(
        email=email,
        password=password_hash,
        name=name
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate JWT token
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'shared_account_id': new_user.shared_account_id
        }
    }), 201


@bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Validation Error', 'message': 'Email and password are required'}), 422
    
    email = data.get('email').strip().lower()
    password = data.get('password')
    
    # Find user by email
    user = User.query.filter_by(email=email).first()
    
    # Verify user exists and password is correct
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'error': 'Unauthorized', 'message': 'Invalid email or password'}), 401
    
    # Generate JWT token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'shared_account_id': user.shared_account_id
        }
    }), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user information"""
    current_user_id = get_jwt_identity()
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'Not Found', 'message': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'shared_account_id': user.shared_account_id,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
    }), 200
