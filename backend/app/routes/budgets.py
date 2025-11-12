from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import BudgetLimit, Category, Expense
from app.auth_utils import get_current_user, shared_account_required, verify_shared_account_access
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from sqlalchemy import func

bp = Blueprint('budgets', __name__, url_prefix='/api/budgets')


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
def get_budgets():
    """Get all budget limits for the user's shared account"""
    current_user = get_current_user()
    
    # Get all budget limits for the shared account
    budget_limits = BudgetLimit.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).all()
    
    return jsonify({
        'budgets': [
            {
                'id': budget.id,
                'category_id': budget.category_id,
                'category_name': budget.category.name if budget.category else None,
                'amount': float(budget.amount),
                'period': budget.period,
                'created_at': budget.created_at.isoformat() if budget.created_at else None,
                'updated_at': budget.updated_at.isoformat() if budget.updated_at else None
            }
            for budget in budget_limits
        ]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
@shared_account_required
def create_budget():
    """Create a new budget limit"""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    required_fields = ['category_id', 'amount', 'period']
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
    
    # Validate period
    period = data.get('period')
    if period not in ['weekly', 'monthly']:
        return jsonify({'error': 'Validation Error', 'message': 'Period must be either "weekly" or "monthly"'}), 422
    
    # Validate category exists and belongs to shared account
    category = Category.query.get(data.get('category_id'))
    if not category:
        return jsonify({'error': 'Not Found', 'message': 'Category not found'}), 404
    
    is_authorized, error_response = verify_shared_account_access(current_user, category.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    # Check if budget limit already exists for this category and period
    existing_budget = BudgetLimit.query.filter_by(
        shared_account_id=current_user.shared_account_id,
        category_id=data.get('category_id'),
        period=period
    ).first()
    
    if existing_budget:
        return jsonify({
            'error': 'Conflict',
            'message': f'Budget limit already exists for this category with {period} period'
        }), 409
    
    # Create budget limit
    new_budget = BudgetLimit(
        shared_account_id=current_user.shared_account_id,
        category_id=data.get('category_id'),
        amount=amount,
        period=period
    )
    
    db.session.add(new_budget)
    db.session.commit()
    
    return jsonify({
        'message': 'Budget limit created successfully',
        'budget': {
            'id': new_budget.id,
            'category_id': new_budget.category_id,
            'category_name': new_budget.category.name if new_budget.category else None,
            'amount': float(new_budget.amount),
            'period': new_budget.period,
            'created_at': new_budget.created_at.isoformat() if new_budget.created_at else None
        }
    }), 201


@bp.route('/<id>', methods=['PUT'])
@jwt_required()
@shared_account_required
def update_budget(id):
    """Update an existing budget limit"""
    current_user = get_current_user()
    
    # Find budget limit
    budget = BudgetLimit.query.get(id)
    if not budget:
        return jsonify({'error': 'Not Found', 'message': 'Budget limit not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, budget.shared_account_id)
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
        budget.amount = amount
    
    # Update period if provided
    if 'period' in data:
        period = data.get('period')
        if period not in ['weekly', 'monthly']:
            return jsonify({'error': 'Validation Error', 'message': 'Period must be either "weekly" or "monthly"'}), 422
        budget.period = period
    
    # Update category if provided
    if 'category_id' in data:
        category = Category.query.get(data.get('category_id'))
        if not category:
            return jsonify({'error': 'Not Found', 'message': 'Category not found'}), 404
        
        # Verify category belongs to same shared account
        if category.shared_account_id != current_user.shared_account_id:
            return jsonify({'error': 'Forbidden', 'message': 'Category does not belong to your shared account'}), 403
        
        budget.category_id = data.get('category_id')
    
    budget.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Budget limit updated successfully',
        'budget': {
            'id': budget.id,
            'category_id': budget.category_id,
            'category_name': budget.category.name if budget.category else None,
            'amount': float(budget.amount),
            'period': budget.period,
            'created_at': budget.created_at.isoformat() if budget.created_at else None,
            'updated_at': budget.updated_at.isoformat() if budget.updated_at else None
        }
    }), 200


@bp.route('/status', methods=['GET'])
@jwt_required()
@shared_account_required
def get_budget_status():
    """Get budget status with spending vs budget for each category and warnings"""
    current_user = get_current_user()
    
    # Get all budget limits for the shared account
    budget_limits = BudgetLimit.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).all()
    
    if not budget_limits:
        return jsonify({
            'budget_status': [],
            'message': 'No budget limits set'
        }), 200
    
    # Calculate date ranges for current period
    today = datetime.utcnow().date()
    
    budget_status = []
    
    for budget in budget_limits:
        # Determine date range based on period
        if budget.period == 'weekly':
            # Start of current week (Monday)
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        else:  # monthly
            # Start of current month
            start_date = today.replace(day=1)
            # End of current month
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        # Calculate total spending for this category in the current period
        total_spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.shared_account_id == current_user.shared_account_id,
            Expense.category_id == budget.category_id,
            Expense.date >= start_date,
            Expense.date <= end_date
        ).scalar() or Decimal('0')
        
        total_spent = float(total_spent)
        budget_amount = float(budget.amount)
        
        # Calculate percentage and remaining
        percentage = (total_spent / budget_amount * 100) if budget_amount > 0 else 0
        remaining = budget_amount - total_spent
        
        # Determine status
        status = 'ok'
        if percentage >= 100:
            status = 'exceeded'
        elif percentage >= 80:
            status = 'warning'
        
        budget_status.append({
            'budget_id': budget.id,
            'category_id': budget.category_id,
            'category_name': budget.category.name if budget.category else None,
            'budget_amount': budget_amount,
            'period': budget.period,
            'spent': total_spent,
            'remaining': remaining,
            'percentage': round(percentage, 2),
            'status': status,
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat()
        })
    
    return jsonify({
        'budget_status': budget_status
    }), 200
