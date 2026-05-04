from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import Customer
from extensions import db

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/')
@login_required
def index():
    active_branch_id = session.get('active_branch_id')
    query = Customer.query
    if active_branch_id:
        query = query.filter(Customer.branch_id == active_branch_id)
        
    customers = query.all()
    return render_template('customers/index.html', customers=customers)

@customers_bp.route('/create', methods=['POST'])
@login_required
def create(): 
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    if name:
        active_branch_id = session.get('active_branch_id')
        customer = Customer(
            name=name, 
            phone=phone, 
            address=address,
            branch_id=active_branch_id or current_user.branch_id
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully.', 'success')
    else:
        flash('Customer name is required.', 'danger')
        
    return redirect(url_for('customers.index'))
