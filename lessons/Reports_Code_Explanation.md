# Line-by-Line Explanation: `routes/reports.py`

This document breaks down the logic used in the Reports module of the **H2Ops** system.

---

## 1. The Imports (Lines 1-8)
```python
from flask import Blueprint, render_template, jsonify, session
from flask_login import login_required
from decorators import admin_required
from models import Sale, Product, SaleItem, User
from sqlalchemy import func
from extensions import db
```
*   **Blueprint**: Declares this file as a module of the main app.
*   **login_required / admin_required**: The "security guards" that ensure only logged-in Admins can see this data.
*   **models (Sale, Product, etc.)**: These are the "Templates" for our database tables.
*   **func**: SQLAlchemy's tool for doing math (aggregations) inside the database.

---

## 2. The Main Page Route (`/`)
This is what happens when you visit the Reports page.

### A. Multi-Branch Context (Lines 16-25)
```python
active_branch_id = session.get('active_branch_id')

rev_q = db.session.query(func.sum(Sale.total_amount))
count_q = db.session.query(func.count(Sale.id))

if active_branch_id:
    rev_q = rev_q.filter(Sale.branch_id == active_branch_id)
    count_q = count_q.filter(Sale.branch_id == active_branch_id)
```
*   **session.get('active_branch_id')**: Retrieves the ID of the branch the Admin is currently viewing.
*   **Query Objects (`rev_q`, `count_q`)**: We create the query first but *don't* execute it yet.
*   **`.filter(...)`**: If there is an active branch, we tell the database to only count sales for that specific branch. This is the core of **Multi-Tenancy architecture**.

### B. Quick Stats
```python
total_revenue = rev_q.scalar() or 0
total_sales_count = count_q.scalar() or 0
avg_order_value = total_revenue / total_sales_count if total_sales_count > 0 else 0
```
*   **`.scalar()`**: Finally executes the filtered query and gives us the number.

### C. Top Products (The Triple Join)
```python
prod_q = db.session.query(
    Product.name, 
    func.sum(SaleItem.quantity).label('total_qty')
).join(SaleItem)

if active_branch_id:
    prod_q = prod_q.join(Sale).filter(Sale.branch_id == active_branch_id)
    
top_products = prod_q.group_by(Product.id).order_by(func.sum(SaleItem.quantity).desc()).limit(5).all()
```
*   **`.join(SaleItem)`**: Connects Product to SaleItem.
*   **`.join(Sale)`**: This is key! We need to join the `Sale` table to check which branch the sale belonged to, because `SaleItem` doesn't have a `branch_id` column itself.
*   **`.group_by(Product.id)`**: Aggregates the quantities.

### D. Staff Performance
```python
cashier_q = db.session.query(
    User.username,
    func.count(Sale.id).label('sale_count'),
    func.sum(Sale.total_amount).label('total_rev')
).join(Sale, User.id == Sale.user_id)

if active_branch_id:
    cashier_q = cashier_q.filter(Sale.branch_id == active_branch_id)
    
cashier_stats = cashier_q.group_by(User.id).all()
```
*   **Filtering**: Ensures that an Admin only sees the performance of staff *within* the selected branch.

---

## 3. The Forecasting API (`/api/forecasting_data`)
This is used by the **Chart.js** graph on your page.

### A. Gathering 30-Day History
```python
for i in range(30, -1, -1):
    d = today - timedelta(days=i)
    sales = Sale.query.filter(db.func.date(Sale.created_at) == d).all()
    totals.append(sum(s.total_amount for s in sales))
```
*   This loop goes back 30 days, finds every sale on that specific date, and adds them up to create a data point for the chart.

### B. Making Predictions
```python
predicted_totals = forecasting.forecast_next_days(totals, days_to_predict=7)
```
*   This sends the last 30 days of totals to our `forecasting.py` script.
*   It uses **Linear Regression** to "draw a line" into the future for the next 7 days.

### C. Sending the Data
```python
return jsonify({ 'historical': ..., 'forecast': ... })
```
*   Converts the Python data into a **JSON** format that the JavaScript in your browser can understand to draw the chart.
