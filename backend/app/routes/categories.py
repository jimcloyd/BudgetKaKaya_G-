from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Category
from app.auth_utils import get_current_user, shared_account_required

bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@bp.route('', methods=['GET'])
@jwt_required()
@shared_account_required
def get_categories():
    """Get all categories for the user's shared account"""
    current_user = get_current_user()
    
    # Get all categories for the shared account
    categories = Category.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).order_by(Category.name).all()
    
    return jsonify({
        'categories': [
            {
                'id': category.id,
                'name': category.name,
                'is_custom': category.is_custom,
                'created_at': category.created_at.isoformat() if category.created_at else None
            }
            for category in categories
        ]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
@shared_account_required
def create_category():
    """Create a custom category for the user's shared account"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('name'):
        return jsonify({'error': 'Validation Error', 'message': 'Category name is required'}), 422
    
    category_name = data.get('name').strip()
    current_user = get_current_user()
    
    # Validate category name is not empty
    if not category_name:
        return jsonify({'error': 'Validation Error', 'message': 'Category name cannot be empty'}), 422
    
    # Check if category name already exists for this shared account (case-insensitive)
    existing_category = Category.query.filter(
        Category.shared_account_id == current_user.shared_account_id,
        db.func.lower(Category.name) == category_name.lower()
    ).first()
    
    if existing_category:
        return jsonify({'error': 'Conflict', 'message': 'Category with this name already exists'}), 409
    
    # Create new custom category
    new_category = Category(
        shared_account_id=current_user.shared_account_id,
        name=category_name,
        is_custom=True
    )
    
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({
        'message': 'Category created successfully',
        'category': {
            'id': new_category.id,
            'name': new_category.name,
            'is_custom': new_category.is_custom,
            'created_at': new_category.created_at.isoformat() if new_category.created_at else None
        }
    }), 201
