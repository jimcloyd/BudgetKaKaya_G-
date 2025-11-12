from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Expense, MonthlyIncome, BudgetLimit, Category, Installment
from app.auth_utils import get_current_user, shared_account_required
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from sqlalchemy import func

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


def calculate_next_payment_date(installment):
    """Calculate the next payment date for an installment"""
    if installment.paid_payments >= installment.number_of_payments:
        return None  # All payments completed
    
    # Next payment is start_date + paid_payments months
    next_date = installment.start_date + relativedelta(months=installment.paid_payments)
    return next_date


def get_budget_status_summary(shared_account_id, today):
    """Get budget status summary for the current period"""
    budget_limits = BudgetLimit.query.filter_by(
        shared_account_id=shared_account_id
    ).all()
    
    if not budget_limits:
        return []
    
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
            Expense.shared_account_id == shared_account_id,
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
            'category_id': budget.category_id,
            'category_name': budget.category.name if budget.category else None,
            'budget_amount': budget_amount,
            'spent': total_spent,
            'remaining': remaining,
            'percentage': round(percentage, 2),
            'status': status
        })
    
    return budget_status


@bp.route('', methods=['GET'])
@jwt_required()
@shared_account_required
def get_dashboard():
    """Get dashboard summary with expenses, income, budget status, and more"""
    current_user = get_current_user()
    today = datetime.utcnow().date()
    
    # Calculate current month date range
    current_month_start = today.replace(day=1)
    if today.month == 12:
        current_month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        current_month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    # Calculate previous month date range for comparison
    if today.month == 1:
        previous_month_start = today.replace(year=today.year - 1, month=12, day=1)
        previous_month_end = today.replace(year=today.year - 1, month=12, day=31)
    else:
        previous_month_start = today.replace(month=today.month - 1, day=1)
        previous_month_end = today.replace(day=1) - timedelta(days=1)
    
    # 1. Calculate total expenses for current month
    current_month_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.shared_account_id == current_user.shared_account_id,
        Expense.date >= current_month_start,
        Expense.date <= current_month_end
    ).scalar() or Decimal('0')
    current_month_expenses = float(current_month_expenses)
    
    # 2. Get monthly income for current month
    current_income = MonthlyIncome.query.filter_by(
        shared_account_id=current_user.shared_account_id,
        month=today.month,
        year=today.year
    ).first()
    
    monthly_income = float(current_income.amount) if current_income else 0
    
    # 3. Calculate net income (income - expenses)
    net_income = monthly_income - current_month_expenses
    
    # 4. Get budget status summary
    budget_status = get_budget_status_summary(current_user.shared_account_id, today)
    
    # 5. Get recent expenses (last 10)
    recent_expenses = Expense.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).order_by(
        Expense.date.desc(),
        Expense.created_at.desc()
    ).limit(10).all()
    
    recent_expenses_list = [
        {
            'id': expense.id,
            'amount': float(expense.amount),
            'category_name': expense.category.name if expense.category else None,
            'date': expense.date.isoformat(),
            'description': expense.description,
            'user_name': expense.user.name if expense.user else None
        }
        for expense in recent_expenses
    ]
    
    # 6. Get upcoming installment payments (due in current month)
    all_installments = Installment.query.filter_by(
        shared_account_id=current_user.shared_account_id
    ).all()
    
    upcoming_installments = []
    for inst in all_installments:
        if inst.paid_payments < inst.number_of_payments:
            next_payment_date = calculate_next_payment_date(inst)
            if next_payment_date and next_payment_date.month == today.month and next_payment_date.year == today.year:
                upcoming_installments.append({
                    'id': inst.id,
                    'description': inst.description,
                    'monthly_payment': float(inst.monthly_payment),
                    'next_payment_date': next_payment_date.isoformat(),
                    'paid_payments': inst.paid_payments,
                    'total_payments': inst.number_of_payments
                })
    
    # 7. Calculate month-over-month spending comparison
    previous_month_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.shared_account_id == current_user.shared_account_id,
        Expense.date >= previous_month_start,
        Expense.date <= previous_month_end
    ).scalar() or Decimal('0')
    previous_month_expenses = float(previous_month_expenses)
    
    # Calculate percentage change
    if previous_month_expenses > 0:
        spending_change_percentage = ((current_month_expenses - previous_month_expenses) / previous_month_expenses) * 100
    else:
        spending_change_percentage = 0 if current_month_expenses == 0 else 100
    
    spending_change = {
        'current_month': current_month_expenses,
        'previous_month': previous_month_expenses,
        'change_amount': current_month_expenses - previous_month_expenses,
        'change_percentage': round(spending_change_percentage, 2)
    }
    
    return jsonify({
        'total_expenses': current_month_expenses,
        'monthly_income': monthly_income,
        'net_income': net_income,
        'budget_status': budget_status,
        'recent_expenses': recent_expenses_list,
        'upcoming_installments': upcoming_installments,
        'spending_comparison': spending_change,
        'current_month': today.month,
        'current_year': today.year
    }), 200
