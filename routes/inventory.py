from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from decorators import admin_required
from models import Product, InventoryLog
from extensions import db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@login_required
@admin_required
def index():
    active_branch_id = session.get('active_branch_id')
    query = Product.query
    if active_branch_id:
        query = query.filter(Product.branch_id == active_branch_id)
        
    products = query.all()
    return render_template('inventory/index.html', products=products)

@inventory_bp.route('/add', methods=['POST'])
@login_required
@admin_required
def add_stock():
    product_id = request.form.get('product_id')
    amount = int(request.form.get('amount', 0))
    reason = request.form.get('reason', 'Manual Restock')
    
    product = Product.query.get(product_id)
    if product and amount > 0:
        product.current_stock += amount
        log = InventoryLog(
            product_id=product.id,
            change_amount=amount,
            log_type='IN',
            reason=reason,
            branch_id=product.branch_id
        )
        db.session.add(log)
        db.session.commit()
        flash('Stock added successfully.', 'success')
    else:
        flash('Invalid amount or product.', 'danger')
        
    return redirect(url_for('inventory.index'))

@inventory_bp.route('/logs')
@login_required
@admin_required
def logs():
    active_branch_id = session.get('active_branch_id')
    query = InventoryLog.query
    if active_branch_id:
        query = query.filter(InventoryLog.branch_id == active_branch_id)
        
    logs = query.order_by(InventoryLog.created_at.desc()).limit(100).all()
    return render_template('inventory/logs.html', logs=logs)
