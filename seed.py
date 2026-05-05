from app import create_app
from extensions import db, bcrypt
from models import User, Product, Customer, Sale, SaleItem, InventoryLog, Branch
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # 1. FORCE RESET (Only for this run to fix your login)
    print("Wiping old data to fix login...")
    db.drop_all()
    db.create_all()

    # 2. Create Branches
    print("Creating branches...")
    b1 = Branch(name='Tagbak Branch', location='Iloilo City')
    b2 = Branch(name='Zarraga Branch', location='Iloilo')
    b3 = Branch(name='Leganes Branch', location='Iloilo')
    db.session.add_all([b1, b2, b3])
    db.session.commit()

    # 3. Create Admin and Staff
    print("Creating users...")
    pw_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    
    # We set your email as the username so you can login with it
    admin = User(
        username='rreynieljosh@gmail.com', 
        password_hash=pw_hash, 
        role='admin', 
        branch_id=b1.id, 
        email='rreynieljosh@gmail.com'
    )
    
    # Staff (Exactly as you wanted them)
    staff_tagbak = User(username='staff_tagbak', password_hash=pw_hash, role='staff', branch_id=b1.id, email='staff_tag@h2ops.com')
    staff_zarraga = User(username='staff_zarraga', password_hash=pw_hash, role='staff', branch_id=b2.id, email='staff_zar@h2ops.com')
    staff_leganes = User(username='staff_leganes', password_hash=pw_hash, role='staff', branch_id=b3.id, email='staff_leg@h2ops.com')
    
    db.session.add_all([admin, staff_tagbak, staff_zarraga, staff_leganes])
    db.session.commit()

    # 4. Create Products
    print("Creating products...")
    branches = [b1, b2, b3]
    for b in branches:
        p1 = Product(name=f'Mineral Water - {b.name}', type='Mineral', price=40.0, current_stock=200, branch_id=b.id)
        db.session.add(p1)
        
    db.session.commit()
    print("DATABASE SEEDED SUCCESSFULLY!")