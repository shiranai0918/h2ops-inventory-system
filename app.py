
import os
from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from extensions import db, bcrypt, login_manager, mail
from models import User, Branch # Ensure models are known to SQLAlchemy

# Import blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.sales import sales_bp
from routes.inventory import inventory_bp
from routes.customers import customers_bp
from routes.reports import reports_bp
from routes.users import users_bp

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()

    # Configure the app
    app.config['SECRET_KEY'] = 'dev-secret-key-h2ops-secure-token-123'
    # Use MySQL on localhost (XAMPP default: root, no password)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp) # main dashboard routes
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(users_bp, url_prefix='/users')
    
    @app.context_processor
    def inject_branches():
        from flask_login import current_user
        if current_user.is_authenticated:
            active_branch_id = session.get('active_branch_id')
            active_branch = Branch.query.get(active_branch_id) if active_branch_id else None
            
            # Admins get to see all branches for switching
            all_branches = Branch.query.all() if current_user.role == 'admin' else []
            
            return dict(
                active_branch=active_branch,
                available_branches=all_branches
            )
        return dict()

    @app.route('/')
    def index():
        return redirect(url_for('main.dashboard'))

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # db.create_all() # We will create tables in seed.py or manually
        pass
    app.run(debug=True, host='0.0.0.0', port=5000)
