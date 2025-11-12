from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import MonthlyIncome, User
from app.auth_utils import get_current_user, shared_account_required, verify_shared_account_access
from datetime import datetime
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import IntegrityError

bp = Blueprint('income', __name__, url_prefix='/api/income')


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


def validate_month(month):
    """Validate that month is between 1 and 12"""
    try:
        month_int = int(month)
        if month_int < 1 or month_int > 12:
            return None, "Month must be between 1 and 12"
        return month_int, None
    except (ValueError, TypeError):
        return None, "Invalid month format"


def validate_year(year):
    """Validate that year is a valid 4-digit year"""
    try:
        year_int = int(year)
        if year_int < 1900 or year_int > 9999:
            return None, "Year must be a valid 4-digit year"
        return year_int, None
    except (ValueError, TypeError):
        return None, "Invalid year format"


@bp.route('', methods=['GET'])
@jwt_required()
@shared_account_required
def get_income():
    """Get monthly income records with optional month/year filtering"""
    current_user = get_current_user()
    
    # Build query
    query = MonthlyIncome.query.filter_by(
        shared_account_id=current_user.shared_account_id
    )
    
    # Apply month filter if provided
    month_param = request.args.get('month')
    if month_param:
        month, error = validate_month(month_param)
        if error:
            return jsonify({'error': 'Validation Error', 'message': f'month: {error}'}), 422
        query = query.filter_by(month=month)
    
    # Apply year filter if provided
    year_param = request.args.get('year')
    if year_param:
        year, error = validate_year(year_param)
        if error:
            return jsonify({'error': 'Validation Error', 'message': f'year: {error}'}), 422
        query = query.filter_by(year=year)
    
    # Order by year and month descending
    incomes = query.order_by(
        MonthlyIncome.year.desc(),
        MonthlyIncome.month.desc()
    ).all()
    
    return jsonify({
        'monthly_incomes': [
            {
                'id': income.id,
                'month': income.month,
                'year': income.year,
                'amount': float(income.amount),
                'created_at': income.created_at.isoformat() if income.created_at else None,
                'updated_at': income.updated_at.isoformat() if income.updated_at else None
            }
            for income in incomes
        ]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
@shared_account_required
def create_income():
    """Set monthly income for a specific month and year"""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    required_fields = ['month', 'year', 'amount']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Validation Error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 422
    
    current_user = get_current_user()
    
    # Validate month
    month, error = validate_month(data.get('month'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': f'month: {error}'}), 422
    
    # Validate year
    year, error = validate_year(data.get('year'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': f'year: {error}'}), 422
    
    # Validate amount
    amount, error = validate_amount(data.get('amount'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': f'amount: {error}'}), 422
    
    # Create monthly income
    new_income = MonthlyIncome(
        shared_account_id=current_user.shared_account_id,
        month=month,
        year=year,
        amount=amount
    )
    
    try:
        db.session.add(new_income)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'error': 'Conflict',
            'message': f'Monthly income for {month}/{year} already exists. Use PUT to update.'
        }), 409
    
    return jsonify({
        'message': 'Monthly income created successfully',
        'monthly_income': {
            'id': new_income.id,
            'month': new_income.month,
            'year': new_income.year,
            'amount': float(new_income.amount),
            'created_at': new_income.created_at.isoformat() if new_income.created_at else None
        }
    }), 201


@bp.route('/<id>', methods=['PUT'])
@jwt_required()
@shared_account_required
def update_income(id):
    """Update an existing monthly income record"""
    current_user = get_current_user()
    
    # Find monthly income
    income = MonthlyIncome.query.get(id)
    if not income:
        return jsonify({'error': 'Not Found', 'message': 'Monthly income not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, income.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    # Update amount if provided
    if 'amount' in data:
        amount, error = validate_amount(data.get('amount'))
        if error:
            return jsonify({'error': 'Validation Error', 'message': f'amount: {error}'}), 422
        income.amount = amount
    
    # Update month if provided
    if 'month' in data:
        month, error = validate_month(data.get('month'))
        if error:
            return jsonify({'error': 'Validation Error', 'message': f'month: {error}'}), 422
        income.month = month
    
    # Update year if provided
    if 'year' in data:
        year, error = validate_year(data.get('year'))
        if error:
            return jsonify({'error': 'Validation Error', 'message': f'year: {error}'}), 422
        income.year = year
    
    income.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'error': 'Conflict',
            'message': f'Monthly income for {income.month}/{income.year} already exists'
        }), 409
    
    return jsonify({
        'message': 'Monthly income updated successfully',
        'monthly_income': {
            'id': income.id,
            'month': income.month,
            'year': income.year,
            'amount': float(income.amount),
            'updated_at': income.updated_at.isoformat() if income.updated_at else None
        }
    }), 200
