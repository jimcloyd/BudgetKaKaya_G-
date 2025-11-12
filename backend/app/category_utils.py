from app import db
from app.models import Category


DEFAULT_CATEGORIES = [
    'groceries',
    'utilities',
    'transportation',
    'entertainment',
    'healthcare',
    'miscellaneous'
]


def seed_default_categories(shared_account_id):
    """
    Seed default categories for a new shared account.
    
    Args:
        shared_account_id: The ID of the shared account to seed categories for
    """
    for category_name in DEFAULT_CATEGORIES:
        # Check if category already exists (to avoid duplicates)
        existing = Category.query.filter_by(
            shared_account_id=shared_account_id,
            name=category_name
        ).first()
        
        if not existing:
            category = Category(
                shared_account_id=shared_account_id,
                name=category_name,
                is_custom=False
            )
            db.session.add(category)
    
    db.session.commit()
