from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import CreditCard, CreditCardTransaction, User
from app.auth_utils import get_current_user, shared_account_required, verify_shared_account_access
from datetime import datetime
from decimal import Decimal, InvalidOperation

bp = Blueprint('credit_cards', __name__, url_prefix='/api/credit-cards')


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
def get_credit_cards():
    """Get all credit cards for the shared account"""
    current_user = get_current_user()
    
    # Get all credit cards for the shared account
    credit_cards = CreditCard.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).order_by(CreditCard.created_at.desc()).all()
    
    return jsonify({
        'credit_cards': [
            {
                'id': card.id,
                'name': card.name,
                'credit_limit': float(card.credit_limit),
                'current_balance': float(card.current_balance),
                'available_credit': float(card.credit_limit - card.current_balance),
                'created_at': card.created_at.isoformat() if card.created_at else None,
                'updated_at': card.updated_at.isoformat() if card.updated_at else None
            }
            for card in credit_cards
        ]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
@shared_account_required
def create_credit_card():
    """Add a new credit card"""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    required_fields = ['name', 'credit_limit', 'current_balance']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Validation Error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 422
    
    current_user = get_current_user()
    
    # Validate credit limit
    credit_limit, error = validate_amount(data.get('credit_limit'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': f'credit_limit: {error}'}), 422
    
    # Validate current balance (can be 0 but not negative)
    try:
        current_balance = Decimal(str(data.get('current_balance')))
        if current_balance < 0:
            return jsonify({'error': 'Validation Error', 'message': 'current_balance cannot be negative'}), 422
        
        # Check for max 2 decimal places
        if current_balance.as_tuple().exponent < -2:
            return jsonify({'error': 'Validation Error', 'message': 'current_balance can have at most 2 decimal places'}), 422
    except (InvalidOperation, ValueError, TypeError):
        return jsonify({'error': 'Validation Error', 'message': 'Invalid current_balance format'}), 422
    
    # Validate name
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Validation Error', 'message': 'name cannot be empty'}), 422
    
    # Create credit card
    new_card = CreditCard(
        shared_account_id=current_user.shared_account_id,
        name=name,
        credit_limit=credit_limit,
        current_balance=current_balance
    )
    
    db.session.add(new_card)
    db.session.commit()
    
    return jsonify({
        'message': 'Credit card created successfully',
        'credit_card': {
            'id': new_card.id,
            'name': new_card.name,
            'credit_limit': float(new_card.credit_limit),
            'current_balance': float(new_card.current_balance),
            'available_credit': float(new_card.credit_limit - new_card.current_balance),
            'created_at': new_card.created_at.isoformat() if new_card.created_at else None
        }
    }), 201


@bp.route('/<id>', methods=['PUT'])
@jwt_required()
@shared_account_required
def update_credit_card(id):
    """Update an existing credit card"""
    current_user = get_current_user()
    
    # Find credit card
    card = CreditCard.query.get(id)
    if not card:
        return jsonify({'error': 'Not Found', 'message': 'Credit card not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, card.shared_account_id)
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
        card.name = name
    
    # Update credit limit if provided
    if 'credit_limit' in data:
        credit_limit, error = validate_amount(data.get('credit_limit'))
        if error:
            return jsonify({'error': 'Validation Error', 'message': f'credit_limit: {error}'}), 422
        card.credit_limit = credit_limit
    
    # Update current balance if provided
    if 'current_balance' in data:
        try:
            current_balance = Decimal(str(data.get('current_balance')))
            if current_balance < 0:
                return jsonify({'error': 'Validation Error', 'message': 'current_balance cannot be negative'}), 422
            
            # Check for max 2 decimal places
            if current_balance.as_tuple().exponent < -2:
                return jsonify({'error': 'Validation Error', 'message': 'current_balance can have at most 2 decimal places'}), 422
            
            card.current_balance = current_balance
        except (InvalidOperation, ValueError, TypeError):
            return jsonify({'error': 'Validation Error', 'message': 'Invalid current_balance format'}), 422
    
    card.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Credit card updated successfully',
        'credit_card': {
            'id': card.id,
            'name': card.name,
            'credit_limit': float(card.credit_limit),
            'current_balance': float(card.current_balance),
            'available_credit': float(card.credit_limit - card.current_balance),
            'created_at': card.created_at.isoformat() if card.created_at else None,
            'updated_at': card.updated_at.isoformat() if card.updated_at else None
        }
    }), 200


@bp.route('/<id>/transactions', methods=['POST'])
@jwt_required()
@shared_account_required
def create_transaction(id):
    """Record a credit card transaction (payment or charge)"""
    current_user = get_current_user()
    
    # Find credit card
    card = CreditCard.query.get(id)
    if not card:
        return jsonify({'error': 'Not Found', 'message': 'Credit card not found'}), 404
    
    # Verify access to shared account
    is_authorized, error_response = verify_shared_account_access(current_user, card.shared_account_id)
    if not is_authorized:
        return jsonify(error_response), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 422
    
    required_fields = ['amount', 'type', 'date']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Validation Error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 422
    
    # Validate amount
    amount, error = validate_amount(data.get('amount'))
    if error:
        return jsonify({'error': 'Validation Error', 'message': error}), 422
    
    # Validate type
    transaction_type = data.get('type', '').lower()
    if transaction_type not in ['payment', 'charge']:
        return jsonify({'error': 'Validation Error', 'message': 'type must be either "payment" or "charge"'}), 422
    
    # Validate and parse date
    try:
        transaction_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'error': 'Validation Error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 422
    
    # Update credit card balance
    if transaction_type == 'payment':
        # Payment reduces balance
        card.current_balance = card.current_balance - amount
        if card.current_balance < 0:
            card.current_balance = Decimal('0')  # Don't allow negative balance
    else:  # charge
        # Charge increases balance
        card.current_balance = card.current_balance + amount
    
    # Create transaction record
    new_transaction = CreditCardTransaction(
        credit_card_id=card.id,
        user_id=current_user.id,
        amount=amount,
        type=transaction_type,
        date=transaction_date,
        description=data.get('description', '').strip() if data.get('description') else None
    )
    
    card.updated_at = datetime.utcnow()
    
    db.session.add(new_transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Transaction recorded successfully',
        'transaction': {
            'id': new_transaction.id,
            'credit_card_id': new_transaction.credit_card_id,
            'amount': float(new_transaction.amount),
            'type': new_transaction.type,
            'date': new_transaction.date.isoformat(),
            'description': new_transaction.description,
            'user_id': new_transaction.user_id,
            'user_name': new_transaction.user.name if new_transaction.user else None,
            'created_at': new_transaction.created_at.isoformat() if new_transaction.created_at else None
        },
        'credit_card': {
            'id': card.id,
            'name': card.name,
            'credit_limit': float(card.credit_limit),
            'current_balance': float(card.current_balance),
            'available_credit': float(card.credit_limit - card.current_balance)
        }
    }), 201
