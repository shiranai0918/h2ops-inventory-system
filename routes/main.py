from flask import Blueprint, render_template, jsonify, session
from flask_login import login_required, current_user
from models import Sale, Product, InventoryLog, Customer, Branch
from extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    active_branch_id = session.get('active_branch_id')
    
    # Base query
    sale_query = Sale.query.filter(db.func.date(Sale.created_at) == today)
    product_query = Product.query
    
    if active_branch_id:
        sale_query = sale_query.filter(Sale.branch_id == active_branch_id)
        product_query = product_query.filter(Product.branch_id == active_branch_id)

    today_sales = sale_query.all()
    total_sales_amount = sum(sale.total_amount for sale in today_sales)
    total_orders = len(today_sales)
    
    # Inventory Alerts
    low_stock_products = product_query.filter(Product.current_stock < 20).all()
    
    # For Admin Branch Switcher
    branches = Branch.query.all() if current_user.role == 'admin' else []
    active_branch = Branch.query.get(active_branch_id) if active_branch_id else None
    
    return render_template('dashboard.html', 
                           total_sales_amount=total_sales_amount, 
                           total_orders=total_orders,
                           low_stock_count=len(low_stock_products),
                           low_stock_products=low_stock_products,
                           branches=branches,
                           active_branch=active_branch)

@main_bp.route('/api/dashboard_data')
@login_required
def dashboard_data():
    # Returns JSON data for charts
    # Daily sales for the last 7 days
    today = datetime.utcnow().date()
    active_branch_id = session.get('active_branch_id')
    days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    
    daily_sales = []
    labels = []
    for d in days:
        query = Sale.query.filter(db.func.date(Sale.created_at) == d)
        if active_branch_id:
            query = query.filter(Sale.branch_id == active_branch_id)
            
        sales = query.all()
        daily_sales.append(sum(s.total_amount for s in sales))
        labels.append(d.strftime('%b %d'))
        
    return jsonify({
        'sales_overview': {
            'labels': labels,
            'data': daily_sales
        }
    })
