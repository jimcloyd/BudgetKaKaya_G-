from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    from app.routes import auth, expenses, categories, budgets, credit_cards, installments, savings, income, account, dashboard
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(expenses.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(budgets.bp)
    app.register_blueprint(credit_cards.bp)
    app.register_blueprint(installments.bp)
    app.register_blueprint(savings.bp)
    app.register_blueprint(income.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(dashboard.bp)

    return app
