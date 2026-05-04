from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', backref='branch', lazy=True)
    customers = db.relationship('Customer', backref='branch', lazy=True)
    products = db.relationship('Product', backref='branch', lazy=True)
    sales = db.relationship('Sale', backref='branch', lazy=True)
    inventory_logs = db.relationship('InventoryLog', backref='branch', lazy=True)


    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) # Added email
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff')  # 'admin' or 'staff'
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

#Unique- Wala dapat sang kapariho (username,password,email)
#Nullable- Kung naka false (dapat ndi sa blanko) kung true pwede ma blanko!(must have data)
#Usermixin- SQLIALCHEMY (Library) - ga hulam ni sya sang logic sa data sa login nga part)
 #power ni sya 1.is_authenticated -kung ang account ga exist sa database)
 #2. is_active -kung ang account active pa )
 #3. is_anonymous -kung ang account anonymous pa )
 #4. is_staff -kung ang account staff pa )
 #5. is_admin -kung ang account admin pa )

# def is_authenticated(self):
#     return True
# def is_active(self):
#     return True
# def is_anonymous(self):
#     return False

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sales = db.relationship('Sale', backref='customer', lazy=True)

#lazy true- kung eh open ta nga button system ta amo lang na ang eh run ya sa database ta nga recorf
#kung naka false bisan wala pata may gina himo ang  tana nga naka record sa database ta eh run ya
# kung naka run basi mag hang or mag lang ang device nga gina gamit sang user. 

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., 'Purified Water', 'Alkaline Water', 'Seal', 'Cap'
    price = db.Column(db.Float, nullable=False)
    current_stock = db.Column(db.Integer, default=0)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sale_items = db.relationship('SaleItem', backref='product', lazy=True)
    inventory_logs = db.relationship('InventoryLog', backref='product', lazy=True)

    # backref- bali sa backref gina call ta ang link between sa mga product.



class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True) # Optional (Walk-in)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Cashier
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False, default='Cash')
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade="all, delete-orphan")
    cashier = db.relationship('User', backref='sales')
    #cascade= may delete eh delete bi ang user sa website kay sala iya na record nga sales

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) # Store current price
    subtotal = db.Column(db.Float, nullable=False)

class InventoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    change_amount = db.Column(db.Integer, nullable=False) # Positive for stock IN, negative for stock OUT
    log_type = db.Column(db.String(20), nullable=False) # 'IN', 'OUT'
    reason = db.Column(db.String(200), nullable=True) # e.g., 'Restock', 'Sale', 'Damage'
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='otps')

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reset_token = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='password_resets')
    
    