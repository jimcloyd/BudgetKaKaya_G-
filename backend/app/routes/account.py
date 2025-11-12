from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, SharedAccount, Invitation
from app.auth_utils import get_current_user
from app.category_utils import seed_default_categories
from datetime import datetime, timedelta

bp = Blueprint('account', __name__, url_prefix='/api/account')


@bp.route('/invite', methods=['POST'])
@jwt_required()
def invite_spouse():
    """Send invitation to spouse to join shared account"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('email'):
        return jsonify({'error': 'Validation Error', 'message': 'Email is required'}), 422
    
    invitee_email = data.get('email').strip().lower()
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({'error': 'Unauthorized', 'message': 'User not found'}), 401
    
    # Validate invitee email is not the same as current user
    if invitee_email == current_user.email:
        return jsonify({'error': 'Validation Error', 'message': 'Cannot invite yourself'}), 422
    
    # Check if invitee exists
    invitee = User.query.filter_by(email=invitee_email).first()
    if not invitee:
        return jsonify({'error': 'Not Found', 'message': 'User with this email does not exist'}), 404
    
    # Check if invitee already has a shared account
    if invitee.shared_account_id:
        return jsonify({'error': 'Conflict', 'message': 'User is already part of a shared account'}), 409
    
    # Create or get shared account for current user
    if not current_user.shared_account_id:
        # Create new shared account
        new_shared_account = SharedAccount()
        db.session.add(new_shared_account)
        db.session.flush()  # Get the ID without committing
        
        # Link current user to shared account
        current_user.shared_account_id = new_shared_account.id
        shared_account_id = new_shared_account.id
        
        # Seed default categories for the new shared account
        seed_default_categories(shared_account_id)
    else:
        shared_account_id = current_user.shared_account_id
        
        # Validate maximum 2 users per shared account
        users_in_account = User.query.filter_by(shared_account_id=shared_account_id).count()
        if users_in_account >= 2:
            return jsonify({'error': 'Conflict', 'message': 'Shared account already has maximum of 2 users'}), 409
    
    # Check for existing pending invitation
    existing_invitation = Invitation.query.filter_by(
        invitee_email=invitee_email,
        shared_account_id=shared_account_id,
        status='pending'
    ).first()
    
    if existing_invitation:
        return jsonify({'error': 'Conflict', 'message': 'Invitation already sent to this user'}), 409
    
    # Create invitation
    invitation = Invitation(
        inviter_id=current_user.id,
        invitee_email=invitee_email,
        shared_account_id=shared_account_id,
        status='pending',
        expires_at=datetime.utcnow() + timedelta(days=7)  # Expires in 7 days
    )
    
    db.session.add(invitation)
    db.session.commit()
    
    return jsonify({
        'message': 'Invitation sent successfully',
        'invitation': {
            'id': invitation.id,
            'invitee_email': invitation.invitee_email,
            'status': invitation.status,
            'created_at': invitation.created_at.isoformat() if invitation.created_at else None,
            'expires_at': invitation.expires_at.isoformat() if invitation.expires_at else None
        }
    }), 201


@bp.route('/accept-invite', methods=['POST'])
@jwt_required()
def accept_invite():
    """Accept invitation to join shared account"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('invitation_id'):
        return jsonify({'error': 'Validation Error', 'message': 'Invitation ID is required'}), 422
    
    invitation_id = data.get('invitation_id')
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({'error': 'Unauthorized', 'message': 'User not found'}), 401
    
    # Check if user already has a shared account
    if current_user.shared_account_id:
        return jsonify({'error': 'Conflict', 'message': 'User is already part of a shared account'}), 409
    
    # Find invitation
    invitation = Invitation.query.get(invitation_id)
    
    if not invitation:
        return jsonify({'error': 'Not Found', 'message': 'Invitation not found'}), 404
    
    # Validate invitation is for current user
    if invitation.invitee_email != current_user.email:
        return jsonify({'error': 'Forbidden', 'message': 'This invitation is not for you'}), 403
    
    # Validate invitation status
    if invitation.status != 'pending':
        return jsonify({'error': 'Conflict', 'message': f'Invitation has already been {invitation.status}'}), 409
    
    # Validate invitation not expired
    if invitation.expires_at < datetime.utcnow():
        invitation.status = 'expired'
        db.session.commit()
        return jsonify({'error': 'Conflict', 'message': 'Invitation has expired'}), 409
    
    # Validate maximum 2 users per shared account
    users_in_account = User.query.filter_by(shared_account_id=invitation.shared_account_id).count()
    if users_in_account >= 2:
        return jsonify({'error': 'Conflict', 'message': 'Shared account already has maximum of 2 users'}), 409
    
    # Link user to shared account
    current_user.shared_account_id = invitation.shared_account_id
    invitation.status = 'accepted'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Invitation accepted successfully',
        'shared_account_id': current_user.shared_account_id
    }), 200


@bp.route('/shared', methods=['GET'])
@jwt_required()
def get_shared_account():
    """Get shared account details with linked users"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({'error': 'Unauthorized', 'message': 'User not found'}), 401
    
    if not current_user.shared_account_id:
        return jsonify({'error': 'Not Found', 'message': 'User is not part of a shared account'}), 404
    
    # Get shared account
    shared_account = SharedAccount.query.get(current_user.shared_account_id)
    
    if not shared_account:
        return jsonify({'error': 'Not Found', 'message': 'Shared account not found'}), 404
    
    # Get all users in shared account
    users = User.query.filter_by(shared_account_id=shared_account.id).all()
    
    return jsonify({
        'shared_account': {
            'id': shared_account.id,
            'created_at': shared_account.created_at.isoformat() if shared_account.created_at else None,
            'users': [
                {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
                for user in users
            ]
        }
    }), 200
