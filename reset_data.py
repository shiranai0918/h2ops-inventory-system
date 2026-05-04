from app import create_app
from extensions import db
from models import Sale, SaleItem, InventoryLog, Product

app = create_app()

with app.app_context():
    print("Resetting database records...")
    
    # Check if we should wipe everything or keep products/users/customers
    # We will keep products, users, and customers, but remove all sales and inventory logs.
    
    # 1. Delete all Sale Items and Sales
    try:
        num_sale_items_deleted = db.session.query(SaleItem).delete()
        num_sales_deleted = db.session.query(Sale).delete()
        
        # 2. Delete all Inventory Logs
        num_inv_logs_deleted = db.session.query(InventoryLog).delete()
        
        # 3. Reset Product stock if desired. Let's set it to 0 or leave it. 
        # Usually, a fresh start might mean setting current_stock = 0.
        # But we can just leave current stock alone or reset to initial. 
        # Let's just delete the history for now.
        
        db.session.commit()
        print(f"Successfully deleted {num_sales_deleted} sales, {num_sale_items_deleted} sale items, and {num_inv_logs_deleted} inventory logs.")
        print("Your database has a clean slate for sales and forecasting!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
