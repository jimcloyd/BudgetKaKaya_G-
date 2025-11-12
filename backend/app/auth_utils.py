from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import User


def get_current_user():
    """
    Helper function to get the current authenticated user from JWT token.
    Returns the User object or None if not found.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    
    user = User.query.get(current_user_id)
    return user


def shared_account_required(f):
    """
    Decorator to verify that the current user has access to a shared account.
    Must be used after @jwt_required() decorator.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        
        if not user:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'User not found'
            }), 401
        
        if not user.shared_account_id:
            return jsonify({
                'error': 'Forbidden',
                'message': 'User must be part of a shared account to access this resource'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def verify_shared_account_access(user, resource_shared_account_id):
    """
    Helper function to verify that a user has access to a specific shared account resource.
    
    Args:
        user: User object
        resource_shared_account_id: The shared_account_id of the resource being accessed
    
    Returns:
        tuple: (is_authorized: bool, error_response: dict or None)
    """
    if not user:
        return False, {'error': 'Unauthorized', 'message': 'User not found'}
    
    if not user.shared_account_id:
        return False, {'error': 'Forbidden', 'message': 'User must be part of a shared account'}
    
    if user.shared_account_id != resource_shared_account_id:
        return False, {'error': 'Forbidden', 'message': 'Access denied to this resource'}
    
    return True, None
