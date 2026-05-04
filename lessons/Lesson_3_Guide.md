# Lesson 3: Database Design — The Foundation of Everything 🧠📦

Welcome to Lesson 3! If the **Routes** are the roadmap of your system, the **Database** is the memory. Without it, your system would "forget" everything as soon as you turned it off.

---

## 1. What is a Database?
A database is a structured collection of data. For H2Ops, we use a **Relational Database** (MySQL). 
- It’s like an Excel workbook where every "Sheet" is a **Table**.
- Every "Row" is a single **Record** (like one specific sale).
- Every "Column" is a piece of information (like the price or the date).

---

## 2. Python talking to Data (SQLAlchemy)
Normally, you have to write complex code (SQL) to talk to a database. But in H2Ops, we use **SQLAlchemy**.
This allows us to treat database tables like **Python Classes**.

Open **[models.py](file:///c:/Projects/Capstone%20System/models.py)**. You will see code like this:
```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
```
SQLAlchemy handles the hard work of translating that Python class into a MySQL table for us.

---

## 3. Relationships: The "Relational" Part 🔗
This is the most important part of your system. Tables "talk" to each other using **Relationships**.

In H2Ops, everything is connected:
1. **Branch ↔ User:** One Branch can have many Users (Staff).
2. **Branch ↔ Sale:** Every Sale must belong to a specific Branch.
3. **Sale ↔ SaleItem:** One Sale can have multiple items (e.g., 2 slim gallons and 1 round gallon).

### The Foreign Key
To connect these, we use a **Foreign Key**. For example, in the `User` table, we have a `branch_id`. This is like a "tag" that says: *"This user belongs to Branch #1."*

---

## 4. Why we use XAMPP?
We use **XAMPP** because it provides the **MySQL Server**—the actual software that stores the data. 
- **Apache:** Serves the website.
- **MySQL:** Manages the memory (the database).
- **phpMyAdmin:** The visual tool we use to "see" the tables in our browser.

---

## ✍️ Practice Task
1. **Check the Schema:** Open **[models.py](file:///c:/Projects/Capstone%20System/models.py)** and find the `InventoryLog` class. 
2. **Identify Columns:** What information do we store when someone adds stock to the system? (Look at the `db.Column` lines).
3. **Visual Check:** Open your XAMPP Control Panel, start MySQL, and go to `http://localhost/phpmyadmin/`. Click on the `h2ops_db` database and look at the tables. Do they match what you see in `models.py`?

---
**Next Up:** *Lesson 4: Routes — The Road Map of Your System*
