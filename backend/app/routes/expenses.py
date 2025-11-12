from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Expense, Category, User
from app.auth_utils import get_current_user, shared_account_required, verify_shared_account_access
from datetime import datetime
from decimal import Decimal, InvalidOperation
from sqlalchemy import func

bp = Blueprint('expenses', __name__, url_prefix='/api/expenses')


def validate_amount(amount_str):
    """Validate that amount is positive with up to 2 decimal places"""
    try:
        amount = Decimal(str(amount_str))
        if amount <= 0:
            return None, "Amount must be positive"
        
        # Check for max 2 decimal places
        if amount.as_tuple().exponent < -2:
            return None, "Amount can have at most 2 decimal places"
        
        return amount, None
    except (InvalidOperation, ValueError, TypeError):
        return None, "Invalid amount format"


@bp.route('', methods=['GET'])
@jwt_required()
@shared_account_required
def get_expenses():
    """Get all expenses with filtering by category, date range, and user"""
    current_user = get_current_user()
    
    # Start with base query for shared account
    query = Expense.query.filter_by(shared_account_id=current_user.shared_account_id)
    
    # Filter by category
    category_id = request.args.get('category_id')
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Filter by user
    user_id = request.args.get('user_id')
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    # Filter by date range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date >= start_date_obj)
        except ValueError:
            return jsonify({'error': 'Validation Error', 'message': 'Invalid start_date format. Use YYYY-MM-DD'}), 422
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date <= end_date_obj)
        except ValueError:
            return jsonify({'error': 'Validation Error', 'message': 'Invalid end_date format. Use YYYY-MM-DD'}), 422
    
    # Order by date descending (most recent first)
    expenses = query.order_by(Expense.date.desc(), Expense.created_at.desc()).all()
    
    return jsonify({
        'expenses': [
            {
                'id': expense.id,
                'amount': float(expense.amount),
                'category_id': expense.category_id,
                'category_name': expense.category.name if expense.category else None,
                'date': expense.date.isoformat(),
                'description': expense.description,
                'user_id': expense.user_id,
                'user_name': expense.user.name if expense.user else None,
                'created_at': expense.created_at.isoformat() if expense.created_at else None,
                'updated_at': expense.updated_at.isoformat() if expense.updated_at else None
            }
            for expense in expenses
        ]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
@shared_account_required
def create_expense():
    """Create a new expense"""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    required_fields = ['amount', 'category_id', 'date']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Validation Error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 422
    
    current_user = get_current_user()
    
    # Validate amount
    amount, error = validate_amount(data.get('amount'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': error}), 422
    
    # Validate category exists and belongs to shared account
    category = Category.query.get(data.get('category_id'))
    if not category:
        return jsonify({'error': 'Not Found', 'message': 'Category not found'}), 404
    
    is_authorized, error_response = verify_shared_account_access(current_user, category.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    # Validate and parse date
    try:
        expense_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'error': 'Validation Error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 422
    
    # Create expense
    new_expense = Expense(
        shared_account_id=current_user.shared_account_id,
        user_id=current_user.id,
        amount=amount,
        category_id=data.get('category_id'),
        date=expense_date,
        description=data.get('description', '').strip() if data.get('description') else None
    )
    
    db.session.add(new_expense)
    db.session.commit()
    
    return jsonify({
        'message': 'Expense created successfully',
        'expense': {
            'id': new_expense.id,
            'amount': float(new_expense.amount),
            'category_id': new_expense.category_id,
            'category_name': new_expense.category.name if new_expense.category else None,
            'date': new_expense.date.isoformat(),
            'description': new_expense.description,
            'user_id': new_expense.user_id,
            'user_name': new_expense.user.name if new_expense.user else None,
            'created_at': new_expense.created_at.isoformat() if new_expense.created_at else None
        }
    }), 201


@bp.route('/<id>', methods=['PUT'])
@jwt_required()
@shared_account_required
def update_expense(id):
    """Update an existing expense"""
    current_user = get_current_user()
    
    # Find expense
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'error': 'Not Found', 'message': 'Expense not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, expense.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    # Update amount if provided
    if 'amount' in data:
        amount, error = validate_amount(data.get('amount'))
        if error:
            return jsonify({'error': 'Validation Error', 'message': error}), 422
        expense.amount = amount
    
    # Update category if provided
    if 'category_id' in data:
        category = Category.query.get(data.get('category_id'))
        if not category:
            return jsonify({'error': 'Not Found', 'message': 'Category not found'}), 404
        
        # Verify category belongs to same shared account
        if category.shared_account_id != current_user.shared_account_id:
            return jsonify({'error': 'Forbidden', 'message': 'Category does not belong to your shared account'}), 403
        
        expense.category_id = data.get('category_id')
    
    # Update date if provided
    if 'date' in data:
        try:
            expense_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
            expense.date = expense_date
        except (ValueError, TypeError):
            return jsonify({'error': 'Validation Error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 422
    
    # Update description if provided
    if 'description' in data:
        expense.description = data.get('description', '').strip() if data.get('description') else None
    
    expense.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Expense updated successfully',
        'expense': {
            'id': expense.id,
            'amount': float(expense.amount),
            'category_id': expense.category_id,
            'category_name': expense.category.name if expense.category else None,
            'date': expense.date.isoformat(),
            'description': expense.description,
            'user_id': expense.user_id,
            'user_name': expense.user.name if expense.user else None,
            'created_at': expense.created_at.isoformat() if expense.created_at else None,
            'updated_at': expense.updated_at.isoformat() if expense.updated_at else None
        }
    }), 200


@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
@shared_account_required
def delete_expense(id):
    """Delete an expense"""
    current_user = get_current_user()
    
    # Find expense
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'error': 'Not Found', 'message': 'Expense not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, expense.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense deleted successfully'}), 200


@bp.route('/summary', methods=['GET'])
@jwt_required()
@shared_account_required
def get_summary():
    """Get expense summary with total spending per category and percentages"""
    current_user = get_current_user()
    
    # Start with base query for shared account
    query = Expense.query.filter_by(shared_account_id=current_user.shared_account_id)
    
    # Filter by date range if provided
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date >= start_date_obj)
        except ValueError:
            return jsonify({'error': 'Validation Error', 'message': 'Invalid start_date format. Use YYYY-MM-DD'}), 422
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Expense.date <= end_date_obj)
        except ValueError:
            return jsonify({'error': 'Validation Error', 'message': 'Invalid end_date format. Use YYYY-MM-DD'}), 422
    
    # Calculate total spending per category with expense count
    category_totals = db.session.query(
        Category.id,
        Category.name,
        func.sum(Expense.amount).label('total'),
        func.count(Expense.id).label('expense_count')
    ).join(
        Expense, Expense.category_id == Category.id
    ).filter(
        Expense.shared_account_id == current_user.shared_account_id
    )
    
    # Apply date filters to the aggregation query
    if start_date:
        category_totals = category_totals.filter(Expense.date >= start_date_obj)
    if end_date:
        category_totals = category_totals.filter(Expense.date <= end_date_obj)
    
    category_totals = category_totals.group_by(Category.id, Category.name).all()
    
    # Calculate grand total
    grand_total = sum(float(total) for _, _, total, _ in category_totals if total)
    
    # Build summary with percentages
    summary = []
    for category_id, category_name, total, expense_count in category_totals:
        if total:
            total_float = float(total)
            percentage = (total_float / grand_total * 100) if grand_total > 0 else 0
            summary.append({
                'category_id': category_id,
                'category_name': category_name,
                'total_amount': total_float,
                'percentage': round(percentage, 2),
                'expense_count': expense_count
            })
    
    # Sort by total descending
    summary.sort(key=lambda x: x['total_amount'], reverse=True)
    
    return jsonify({
        'summary': summary,
        'grand_total': grand_total,
        'start_date': start_date,
        'end_date': end_date
    }), 200
