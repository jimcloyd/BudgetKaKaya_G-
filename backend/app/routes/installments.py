from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Installment, User
from app.auth_utils import get_current_user, shared_account_required, verify_shared_account_access
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, InvalidOperation

bp = Blueprint('installments', __name__, url_prefix='/api/installments')


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


def calculate_next_payment_date(installment):
    """Calculate the next payment date for an installment"""
    if installment.paid_payments >= installment.number_of_payments:
        return None  # All payments completed
    
    # Next payment is start_date + paid_payments months
    next_date = installment.start_date + relativedelta(months=installment.paid_payments)
    return next_date


def calculate_remaining_balance(installment):
    """Calculate the remaining balance for an installment"""
    remaining_payments = installment.number_of_payments - installment.paid_payments
    remaining_balance = installment.monthly_payment * remaining_payments
    return remaining_balance


@bp.route('', methods=['GET'])
@jwt_required()
@shared_account_required
def get_installments():
    """Get all installments for the shared account"""
    current_user = get_current_user()
    
    # Get all installments for the shared account
    installments = Installment.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).order_by(Installment.created_at.desc()).all()
    
    return jsonify({
        'installments': [
            {
                'id': inst.id,
                'total_amount': float(inst.total_amount),
                'number_of_payments': inst.number_of_payments,
                'monthly_payment': float(inst.monthly_payment),
                'start_date': inst.start_date.isoformat(),
                'description': inst.description,
                'paid_payments': inst.paid_payments,
                'remaining_balance': float(calculate_remaining_balance(inst)),
                'next_payment_date': calculate_next_payment_date(inst).isoformat() if calculate_next_payment_date(inst) else None,
                'user_id': inst.user_id,
                'user_name': inst.user.name if inst.user else None,
                'created_at': inst.created_at.isoformat() if inst.created_at else None,
                'updated_at': inst.updated_at.isoformat() if inst.updated_at else None
            }
            for inst in installments
        ]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
@shared_account_required
def create_installment():
    """Create a new installment"""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    required_fields = ['total_amount', 'number_of_payments', 'start_date', 'description']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Validation Error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 422
    
    current_user = get_current_user()
    
    # Validate total amount
    total_amount, error = validate_amount(data.get('total_amount'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': f'total_amount: {error}'}), 422
    
    # Validate number of payments
    try:
        number_of_payments = int(data.get('number_of_payments'))
        if number_of_payments <= 0:
            return jsonify({'error': 'Validation Error', 'message': 'number_of_payments must be positive'}), 422
    except (ValueError, TypeError):
        return jsonify({'error': 'Validation Error', 'message': 'Invalid number_of_payments format'}), 422
    
    # Validate and parse start date
    try:
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'error': 'Validation Error', 'message': 'Invalid start_date format. Use YYYY-MM-DD'}), 422
    
    # Validate description
    description = data.get('description', '').strip()
    if not description:
        return jsonify({'error': 'Validation Error', 'message': 'description cannot be empty'}), 422
    
    # Calculate monthly payment
    monthly_payment = total_amount / number_of_payments
    # Round to 2 decimal places
    monthly_payment = monthly_payment.quantize(Decimal('0.01'))
    
    # Create installment
    new_installment = Installment(
        shared_account_id=current_user.shared_account_id,
        user_id=current_user.id,
        total_amount=total_amount,
        number_of_payments=number_of_payments,
        monthly_payment=monthly_payment,
        start_date=start_date,
        description=description,
        paid_payments=0
    )
    
    db.session.add(new_installment)
    db.session.commit()
    
    return jsonify({
        'message': 'Installment created successfully',
        'installment': {
            'id': new_installment.id,
            'total_amount': float(new_installment.total_amount),
            'number_of_payments': new_installment.number_of_payments,
            'monthly_payment': float(new_installment.monthly_payment),
            'start_date': new_installment.start_date.isoformat(),
            'description': new_installment.description,
            'paid_payments': new_installment.paid_payments,
            'remaining_balance': float(calculate_remaining_balance(new_installment)),
            'next_payment_date': calculate_next_payment_date(new_installment).isoformat() if calculate_next_payment_date(new_installment) else None,
            'user_id': new_installment.user_id,
            'user_name': new_installment.user.name if new_installment.user else None,
            'created_at': new_installment.created_at.isoformat() if new_installment.created_at else None
        }
    }), 201


@bp.route('/<id>/pay', methods=['POST'])
@jwt_required()
@shared_account_required
def mark_payment(id):
    """Mark an installment payment as completed"""
    current_user = get_current_user()
    
    # Find installment
    installment = Installment.query.get(id)
    if not installment:
        return jsonify({'error': 'Not Found', 'message': 'Installment not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, installment.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    # Check if all payments are already completed
    if installment.paid_payments >= installment.number_of_payments:
        return jsonify({
            'error': 'Validation Error',
            'message': 'All payments for this installment have already been completed'
        }), 422
    
    # Increment paid payments
    installment.paid_payments += 1
    installment.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Payment marked as completed',
        'installment': {
            'id': installment.id,
            'total_amount': float(installment.total_amount),
            'number_of_payments': installment.number_of_payments,
            'monthly_payment': float(installment.monthly_payment),
            'start_date': installment.start_date.isoformat(),
            'description': installment.description,
            'paid_payments': installment.paid_payments,
            'remaining_balance': float(calculate_remaining_balance(installment)),
            'next_payment_date': calculate_next_payment_date(installment).isoformat() if calculate_next_payment_date(installment) else None,
            'user_id': installment.user_id,
            'user_name': installment.user.name if installment.user else None,
            'updated_at': installment.updated_at.isoformat() if installment.updated_at else None
        }
    }), 200
