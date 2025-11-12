from app import db
from datetime import datetime
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shared_account = db.relationship('SharedAccount', backref='users', foreign_keys=[shared_account_id])
    expenses = db.relationship('Expense', backref='user', lazy=True)
    invitations_sent = db.relationship('Invitation', backref='inviter', foreign_keys='Invitation.inviter_id', lazy=True)
    credit_card_transactions = db.relationship('CreditCardTransaction', backref='user', lazy=True)
    installments = db.relationship('Installment', backref='user', lazy=True)
    savings_contributions = db.relationship('SavingsContribution', backref='user', lazy=True)


class SharedAccount(db.Model):
    __tablename__ = 'shared_accounts'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invitations = db.relationship('Invitation', backref='shared_account', lazy=True)
    categories = db.relationship('Category', backref='shared_account', lazy=True)
    expenses = db.relationship('Expense', backref='shared_account', lazy=True)
    budget_limits = db.relationship('BudgetLimit', backref='shared_account', lazy=True)
    credit_cards = db.relationship('CreditCard', backref='shared_account', lazy=True)
    installments = db.relationship('Installment', backref='shared_account', lazy=True)
    savings_goals = db.relationship('SavingsGoal', backref='shared_account', lazy=True)
    monthly_incomes = db.relationship('MonthlyIncome', backref='shared_account', lazy=True)


class Invitation(db.Model):
    __tablename__ = 'invitations'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    inviter_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    invitee_email = db.Column(db.String(255), nullable=False)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Relationships are defined via backref in User and SharedAccount models


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_custom = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='category', lazy=True)
    budget_limits = db.relationship('BudgetLimit', backref='category', lazy=True)


class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships are defined via backref in User, SharedAccount, and Category models


class BudgetLimit(db.Model):
    __tablename__ = 'budget_limits'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships are defined via backref in SharedAccount and Category models


class CreditCard(db.Model):
    __tablename__ = 'credit_cards'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    credit_limit = db.Column(db.Numeric(10, 2), nullable=False)
    current_balance = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('CreditCardTransaction', backref='credit_card', lazy=True)


class CreditCardTransaction(db.Model):
    __tablename__ = 'credit_card_transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    credit_card_id = db.Column(db.String(36), db.ForeignKey('credit_cards.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships are defined via backref in CreditCard and User models


class Installment(db.Model):
    __tablename__ = 'installments'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    number_of_payments = db.Column(db.Integer, nullable=False)
    monthly_payment = db.Column(db.Numeric(10, 2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    paid_payments = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships are defined via backref in SharedAccount and User models


class SavingsGoal(db.Model):
    __tablename__ = 'savings_goals'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    target_amount = db.Column(db.Numeric(10, 2), nullable=False)
    current_balance = db.Column(db.Numeric(10, 2), default=0)
    target_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contributions = db.relationship('SavingsContribution', backref='savings_goal', lazy=True)


class SavingsContribution(db.Model):
    __tablename__ = 'savings_contributions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    savings_goal_id = db.Column(db.String(36), db.ForeignKey('savings_goals.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships are defined via backref in SavingsGoal and User models


class MonthlyIncome(db.Model):
    __tablename__ = 'monthly_income'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('shared_account_id', 'month', 'year'),)
    
    # Relationships are defined via backref in SharedAccount model


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='password_reset_tokens')
