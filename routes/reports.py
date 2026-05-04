from flask import Blueprint, render_template, jsonify, session
from flask_login import login_required
from decorators import admin_required
from models import Sale, Product, SaleItem, User, Branch
from sqlalchemy import func
from extensions import db
from datetime import datetime, timedelta
import forecasting

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
@admin_required
def index():
    active_branch_id = session.get('active_branch_id')
    
    # 1. Quick Stats (All Time)
    rev_q = db.session.query(func.sum(Sale.total_amount))
    count_q = db.session.query(func.count(Sale.id))
    
    if active_branch_id:
        rev_q = rev_q.filter(Sale.branch_id == active_branch_id)
        count_q = count_q.filter(Sale.branch_id == active_branch_id)
        
    total_revenue = rev_q.scalar() or 0
    total_sales_count = count_q.scalar() or 0
    avg_order_value = total_revenue / total_sales_count if total_sales_count > 0 else 0

    # 2. Top 3 Branches (Mineral Water)
    branch_q = db.session.query(
        Branch.name, 
        func.sum(SaleItem.quantity).label('total_qty')
    ).select_from(Branch).join(Sale).join(SaleItem).join(Product, SaleItem.product_id == Product.id).filter(
        Product.name.ilike('%mineral%')
    )
    
    if active_branch_id:
        branch_q = branch_q.filter(Sale.branch_id == active_branch_id)
        
    top_branches = branch_q.group_by(Branch.id).order_by(func.sum(SaleItem.quantity).desc()).limit(3).all()

    # 3. Sales by Cashier
    cashier_q = db.session.query(
        User.username,
        func.count(Sale.id).label('sale_count'),
        func.sum(Sale.total_amount).label('total_rev')
    ).join(Sale, User.id == Sale.user_id)
    
    if active_branch_id:
        cashier_q = cashier_q.filter(Sale.branch_id == active_branch_id)
        
    cashier_stats = cashier_q.group_by(User.id).all()

    return render_template('reports/index.html', 
                           total_revenue=total_revenue,
                           total_sales_count=total_sales_count,
                           avg_order_value=avg_order_value,
                           top_branches=top_branches,
                           cashier_stats=cashier_stats)

@reports_bp.route('/api/forecasting_data')
@login_required
@admin_required
def forecasting_data():
    # Gather historical daily sales for the past 30 days
    today = datetime.utcnow().date()
    active_branch_id = session.get('active_branch_id')
    historical_days = 30
    
    dates = []
    totals = []
    for i in range(historical_days, -1, -1):
        d = today - timedelta(days=i)
        query = Sale.query.filter(db.func.date(Sale.created_at) == d)
        if active_branch_id:
            query = query.filter(Sale.branch_id == active_branch_id)
            
        sales = query.all()
        dates.append(d.strftime('%b %d'))
        totals.append(sum(s.total_amount for s in sales))
        
    # Make forecasts for the next 7 days
    predicted_totals = forecasting.forecast_next_days(totals, days_to_predict=7)
    predicted_dates = [(today + timedelta(days=i)).strftime('%b %d') for i in range(1, 8)]
    
    # We want to stitch them to show a continuous chart
    return jsonify({
        'historical': {
            'labels': dates,
            'data': totals
        },
        'forecast': {
            'labels': predicted_dates,
            'data': predicted_totals
        }
    })
