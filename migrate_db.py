from app import create_app
from extensions import db, bcrypt
from models import User, Branch
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError

app = create_app()

# ==========================================
# SET YOUR REAL CREDENTIALS HERE
# ==========================================
ADMIN_GMAIL = 'princejohnbundalan1@gmail.com'
ADMIN_PASSWORD = 'password123'

STAFF_GMAIL = 'prbe.bundalan.ui@phinmaed.com'
STAFF_PASSWORD = 'password1234'
# ==========================================

with app.app_context():
    print("Starting database migration and account setup...")
    
    # 1. Add email column to user table safely
    try:
        db.session.execute(text("ALTER TABLE user ADD COLUMN email VARCHAR(120) UNIQUE DEFAULT NULL"))
        db.session.commit()
    except Exception:
        db.session.rollback()

    # 2. Add branch_id column to existing tables safely
    tables_to_update = ['user', 'customer', 'product', 'sale', 'inventory_log']
    for table in tables_to_update:
        try:
            db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN branch_id INTEGER REFERENCES branch(id)"))
            db.session.commit()
        except Exception:
            db.session.rollback()

    # 3. Create Default Branches if they don't exist
    branches = [
        {'name': 'Tagbak Branch', 'location': 'Iloilo City'},
        {'name': 'Zarraga Branch', 'location': 'Iloilo'},
        {'name': 'Leganes Branch', 'location': 'Iloilo'}
    ]
    
    # Ensure branch table exists first
    db.create_all()

    for b_data in branches:
        if not Branch.query.filter_by(name=b_data['name']).first():
            new_branch = Branch(name=b_data['name'], location=b_data['location'])
            db.session.add(new_branch)
    db.session.commit()

    main_branch = Branch.query.filter_by(name='Tagbak Branch').first()

    # Update Admin
    admin = User.query.filter_by(role='admin').first()
    if admin:
        admin.email = ADMIN_GMAIL
        admin.password_hash = bcrypt.generate_password_hash(ADMIN_PASSWORD).decode('utf-8')
        
    # Update Staff
    staff = User.query.filter_by(role='staff').first()
    if staff:
        staff.email = STAFF_GMAIL
        staff.password_hash = bcrypt.generate_password_hash(STAFF_PASSWORD).decode('utf-8')
        staff.branch_id = main_branch.id if main_branch else None
        
    # Link Admin too
    if admin:
        admin.branch_id = main_branch.id if main_branch else None

    # Link all existing data to Main Branch as a fallback
    if main_branch:
        from models import Product, Customer, Sale, InventoryLog
        Product.query.filter(Product.branch_id == None).update({Product.branch_id: main_branch.id})
        Customer.query.filter(Customer.branch_id == None).update({Customer.branch_id: main_branch.id})
        # Note: bulk updates might be faster but this is fine for migration
        Sale.query.filter(Sale.branch_id == None).update({Sale.branch_id: main_branch.id})
        InventoryLog.query.filter(InventoryLog.branch_id == None).update({InventoryLog.branch_id: main_branch.id})
        
    db.session.commit()
    print(f"Accounts updated! Admin: {ADMIN_GMAIL}, Staff: {STAFF_GMAIL}")

    # 2. Create new tables
    db.create_all()
    print("Migration complete!")
