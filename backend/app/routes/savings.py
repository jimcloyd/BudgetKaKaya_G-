from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import SavingsGoal, SavingsContribution, User
from app.auth_utils import get_current_user, shared_account_required, verify_shared_account_access
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, InvalidOperation

bp = Blueprint('savings', __name__, url_prefix='/api/savings-goals')


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


def calculate_goal_metrics(goal):
    """Calculate metrics for a savings goal"""
    # Calculate percentage completed
    percentage_completed = 0
    if goal.target_amount > 0:
        percentage_completed = (float(goal.current_balance) / float(goal.target_amount)) * 100
        percentage_completed = min(percentage_completed, 100)  # Cap at 100%
    
    # Calculate remaining amount
    remaining_amount = max(float(goal.target_amount) - float(goal.current_balance), 0)
    
    # Calculate suggested monthly contribution if target date exists
    suggested_monthly_contribution = None
    if goal.target_date and remaining_amount > 0:
        today = datetime.utcnow().date()
        if goal.target_date > today:
            # Calculate months until target date
            months_remaining = (goal.target_date.year - today.year) * 12 + (goal.target_date.month - today.month)
            if months_remaining > 0:
                suggested_monthly_contribution = remaining_amount / months_remaining
    
    return {
        'percentage_completed': round(percentage_completed, 2),
        'remaining_amount': remaining_amount,
        'suggested_monthly_contribution': round(suggested_monthly_contribution, 2) if suggested_monthly_contribution else None
    }


@bp.route('', methods=['GET'])
@jwt_required()
@shared_account_required
def get_savings_goals():
    """Get all savings goals for the shared account"""
    current_user = get_current_user()
    
    # Get all savings goals for the shared account
    goals = SavingsGoal.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).order_by(SavingsGoal.created_at.desc()).all()
    
    return jsonify({
        'savings_goals': [
            {
                'id': goal.id,
                'name': goal.name,
                'target_amount': float(goal.target_amount),
                'current_balance': float(goal.current_balance),
                'target_date': goal.target_date.isoformat() if goal.target_date else None,
                **calculate_goal_metrics(goal),
                'created_at': goal.created_at.isoformat() if goal.created_at else None,
                'updated_at': goal.updated_at.isoformat() if goal.updated_at else None
            }
            for goal in goals
        ]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
@shared_account_required
def create_savings_goal():
    """Create a new savings goal"""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    required_fields = ['name', 'target_amount']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Validation Error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 422
    
    current_user = get_current_user()
    
    # Validate name
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Validation Error', 'message': 'name cannot be empty'}), 422
    
    # Validate target amount
    target_amount, error = validate_amount(data.get('target_amount'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': f'target_amount: {error}'}), 422
    
    # Validate and parse target date (optional)
    target_date = None
    if 'target_date' in data and data.get('target_date'):
        try:
            target_date = datetime.strptime(data.get('target_date'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return jsonify({'error': 'Validation Error', 'message': 'Invalid target_date format. Use YYYY-MM-DD'}), 422
    
    # Create savings goal
    new_goal = SavingsGoal(
        shared_account_id=current_user.shared_account_id,
        name=name,
        target_amount=target_amount,
        current_balance=0,
        target_date=target_date
    )
    
    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({
        'message': 'Savings goal created successfully',
        'savings_goal': {
            'id': new_goal.id,
            'name': new_goal.name,
            'target_amount': float(new_goal.target_amount),
            'current_balance': float(new_goal.current_balance),
            'target_date': new_goal.target_date.isoformat() if new_goal.target_date else None,
            **calculate_goal_metrics(new_goal),
            'created_at': new_goal.created_at.isoformat() if new_goal.created_at else None
        }
    }), 201


@bp.route('/<id>', methods=['PUT'])
@jwt_required()
@shared_account_required
def update_savings_goal(id):
    """Update an existing savings goal"""
    current_user = get_current_user()
    
    # Find savings goal
    goal = SavingsGoal.query.get(id)
    if not goal:
        return jsonify({'error': 'Not Found', 'message': 'Savings goal not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, goal.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    # Update name if provided
    if 'name' in data:
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'error': 'Validation Error', 'message': 'name cannot be empty'}), 422
        goal.name = name
    
    # Update target amount if provided
    if 'target_amount' in data:
        target_amount, error = validate_amount(data.get('target_amount'))
        if error:
            return jsonify({'error': 'Validation Error', 'message': f'target_amount: {error}'}), 422
        goal.target_amount = target_amount
    
    # Update target date if provided
    if 'target_date' in data:
        if data.get('target_date') is None:
            goal.target_date = None
        else:
            try:
                goal.target_date = datetime.strptime(data.get('target_date'), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return jsonify({'error': 'Validation Error', 'message': 'Invalid target_date format. Use YYYY-MM-DD'}), 422
    
    goal.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Savings goal updated successfully',
        'savings_goal': {
            'id': goal.id,
            'name': goal.name,
            'target_amount': float(goal.target_amount),
            'current_balance': float(goal.current_balance),
            'target_date': goal.target_date.isoformat() if goal.target_date else None,
            **calculate_goal_metrics(goal),
            'updated_at': goal.updated_at.isoformat() if goal.updated_at else None
        }
    }), 200


@bp.route('/<id>/contributions', methods=['POST'])
@jwt_required()
@shared_account_required
def add_contribution(id):
    """Add a contribution to a savings goal"""
    current_user = get_current_user()
    
    # Find savings goal
    goal = SavingsGoal.query.get(id)
    if not goal:
        return jsonify({'error': 'Not Found', 'message': 'Savings goal not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, goal.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    # Validate required fields
    required_fields = ['amount', 'date']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Validation Error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 422
    
    # Validate amount
    amount, error = validate_amount(data.get('amount'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': f'amount: {error}'}), 422
    
    # Validate and parse date
    try:
        contribution_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'error': 'Validation Error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 422
    
    # Create contribution
    new_contribution = SavingsContribution(
        savings_goal_id=goal.id,
        user_id=current_user.id,
        amount=amount,
        date=contribution_date
    )
    
    # Update savings goal current_balance
    goal.current_balance += amount
    goal.updated_at = datetime.utcnow()
    
    db.session.add(new_contribution)
    db.session.commit()
    
    # Calculate updated metrics
    metrics = calculate_goal_metrics(goal)
    
    return jsonify({
        'message': 'Contribution added successfully',
        'contribution': {
            'id': new_contribution.id,
            'amount': float(new_contribution.amount),
            'date': new_contribution.date.isoformat(),
            'user_id': new_contribution.user_id,
            'user_name': new_contribution.user.name if new_contribution.user else None,
            'created_at': new_contribution.created_at.isoformat() if new_contribution.created_at else None
        },
        'savings_goal': {
            'id': goal.id,
            'name': goal.name,
            'target_amount': float(goal.target_amount),
            'current_balance': float(goal.current_balance),
            'target_date': goal.target_date.isoformat() if goal.target_date else None,
            **metrics,
            'updated_at': goal.updated_at.isoformat() if goal.updated_at else None
        }
    }), 201
