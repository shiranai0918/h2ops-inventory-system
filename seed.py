from app import create_app
from extensions import db, bcrypt
from models import User, Product, Customer, Sale, SaleItem, InventoryLog, Branch

app = create_app()

with app.app_context():
    db.create_all()

    print("Checking and seeding branches...")
    # Get or create branches to prevent duplication errors
    b1 = Branch.query.filter_by(name='Tagbak Branch').first() or Branch(name='Tagbak Branch', location='Iloilo City')
    b2 = Branch.query.filter_by(name='Zarraga Branch').first() or Branch(name='Zarraga Branch', location='Iloilo')
    b3 = Branch.query.filter_by(name='Leganes Branch').first() or Branch(name='Leganes Branch', location='Iloilo')
    
    db.session.add_all([b1, b2, b3])
    db.session.commit()

    print("Checking and seeding users...")
    pw_hash = bcrypt.generate_password_hash('password123').decode('utf-8')

    # ADMIN: Ensuring username is the email you want to use for login
    admin = User.query.filter_by(email='rreynieljosh@gmail.com').first()
    if not admin:
        admin = User(
            username='rreynieljosh@gmail.com', 
            password_hash=pw_hash, 
            role='admin', 
            branch_id=b1.id, 
            email='rreynieljosh@gmail.com'
        )
        db.session.add(admin)
    else:
        # Update existing admin to ensure password and username match
        admin.username = 'rreynieljosh@gmail.com'
        admin.password_hash = pw_hash

    # STAFF: Kept exactly as you specified
    staff_list = [
        {'un': 'staff_tagbak', 'em': 'staff_tag@h2ops.com', 'br': b1.id},
        {'un': 'staff_zarraga', 'em': 'staff_zar@h2ops.com', 'br': b2.id},
        {'un': 'staff_leganes', 'em': 'staff_leg@h2ops.com', 'br': b3.id}
    ]

    for s in staff_list:
        user = User.query.filter_by(username=s['un']).first()
        if not user:
            user = User(username=s['un'], password_hash=pw_hash, role='staff', branch_id=s['br'], email=s['em'])
            db.session.add(user)

    db.session.commit()

    print("Checking products...")
    for b in [b1, b2, b3]:
        p_name = f'Mineral Water - {b.name}'
        if not Product.query.filter_by(name=p_name).first():
            p1 = Product(name=p_name, type='Mineral', price=40.0, current_stock=200, branch_id=b.id)
            db.session.add(p1)

    db.session.commit()
    print("Surgical seed successful. System ready.")