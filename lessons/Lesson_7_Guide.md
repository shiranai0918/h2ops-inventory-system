# Lesson 7: Advanced Queries & Reporting — Business Intelligence

## 📌 Overview
In this lesson, we transform the **H2Ops** system from a simple transaction recorder into a decision-making tool. We move beyond fetching single records and start performing **Data Aggregation**—summarizing thousands of rows into meaningful business metrics.

## 🎯 Learning Objectives
1. **Understand Aggregations**: Use `SUM`, `COUNT`, and `AVG` in SQLAlchemy.
2. **Master Relationships**: Perform `Joins` between Sales, Items, and Products.
3. **Data Grouping**: Use `GROUP_BY` to categorize data (e.g., Sales by Staff).
4. **Multi-Branch Filtering**: Learn how to filter global data into branch-specific reports using Session storage.
5. **Business ROI**: Understand why comparing branch performance matters for growth.

---

## 🛠️ Step 1: The Backend Logic (`routes/reports.py`)
To generate reports, we use the `sqlalchemy.func` module. This allows the database to do the heavy lifting (math) instead of Python.

### The Key Queries:
1. **Total Revenue (Branch-Aware)**: 
   Now filtered using `Sale.branch_id == active_branch_id`.
2. **Top Products (Triple Join)**:
   This now requires joining `Product`, `SaleItem`, AND `Sale` to filter by the branch where the sale occurred.
3. **Staff Performance**:
   Joining `User` with `Sale` to count how many orders each staff member handled for the specific branch.

---

## 🎨 Step 2: The Visual Interface (`templates/reports/index.html`)
A report is only useful if it's readable. We use a **Grid Layout** to display "Quick Stats" at the top, followed by detailed tables.

### Key BI Metrics to Display:
- **Total Revenue**: Gross income of the station.
- **Sales Count**: Volume of transactions.
- **Average Order Value (AOV)**: Revenue divided by Sales Count.
- **Top 5 Products**: Identifies inventory priorities.
- **Staff Performance Table**: Monitors cashier activity and accountability.

---

## 💻 Code Snippets for Implementation

### 1. Update Imports in `routes/reports.py`
Ensure `User` and `func` are available:
```python
from models import User, Sale, Product, SaleItem
from sqlalchemy import func
```

### 2. The Updated Route Logic
```python
@reports_bp.route('/')
@login_required
@admin_required
def index():
    # 1. Get the current active branch from the session (Multi-Branch Logic)
    active_branch_id = session.get('active_branch_id')
    
    # 2. Base Queries (Quick Stats)
    rev_q = db.session.query(func.sum(Sale.total_amount))
    count_q = db.session.query(func.count(Sale.id))
    
    # 3. Apply Multi-Branch Filtering
    if active_branch_id:
        rev_q = rev_q.filter(Sale.branch_id == active_branch_id)
        count_q = count_q.filter(Sale.branch_id == active_branch_id)
        
    total_revenue = rev_q.scalar() or 0
    total_sales_count = count_q.scalar() or 0
    avg_order_value = total_revenue / total_sales_count if total_sales_count > 0 else 0

    # 4. Top 5 Products (Filtered by Branch)
    prod_q = db.session.query(
        Product.name, 
        func.sum(SaleItem.quantity).label('total_qty')
    ).join(SaleItem)
    
    if active_branch_id:
        # We join Sale here because SaleItem only knows the Product,
        # but Sale knows the Branch.
        prod_q = prod_q.join(Sale).filter(Sale.branch_id == active_branch_id)
        
    top_products = prod_q.group_by(Product.id).order_by(func.sum(SaleItem.quantity).desc()).limit(5).all()

    # 5. Sales by Cashier (Filtered by Branch)
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
                           top_products=top_products,
                           cashier_stats=cashier_stats)
```

---

## 💡 Why is this "Business Intelligence"?
By identifying that **Alkaline Water** is your top-selling product, you know to stock more alkaline filters. By seeing that **Staff X** handles 70% of sales, you can optimize shift schedules. This is how data becomes intelligence.
