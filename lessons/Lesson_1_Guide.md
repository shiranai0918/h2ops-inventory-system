# Lesson 1: Introduction & Environment Setup 🚀

Welcome to the first lesson of your Capstone journey! In this lesson, we will explore what **H2Ops** is, why it's built the way it is, and how to get your professional development environment ready.

---

## 1. What is H2Ops?
**H2Ops** (Water Operations) is a cloud-based management system designed for **Water Refilling Stations**. 

### The Problem
Most small-to-medium water businesses manage their sales, inventory, and branches using manual logbooks. This leads to:
- **Human Error:** Calculations in logbooks are often wrong.
- **Lack of Real-time Data:** Owners don't know how much stock is left until they physically check.
- **Multi-branch Chaos:** Managing three different locations from one spot is nearly impossible without a digital system.

### The H2Ops Solution
Our system provides:
1. **Multi-Branch Support:** One dashboard to monitor all locations.
2. **Real-time Inventory:** Automatically updates stock when a sale is made.
3. **Advanced Reporting:** Visual charts showing which branch is performing best.
4. **Role-based Access:** Admins can see everything; Staff can only see their branch.

---

## 2. The Technology Stack
We use a modern, reliable stack that is perfect for business applications:

| Technology | Role | Why? |
| :--- | :--- | :--- |
| **Python** | Logic | Easy to read, powerful libraries for data. |
| **Flask** | Web Framework | Lightweight and flexible for custom systems. |
| **MySQL (XAMPP)** | Database | Relational database perfect for complex data (Sales, Logs). |
| **Jinja2** | Templating | Allows us to inject Python data directly into HTML. |
| **Vanilla CSS** | Styling | Full control over the premium design without bloat. |

---

## 3. Setting Up Your "Lab"
Follow these steps to ensure your system is ready for development.

### Step A: Virtual Environment (The Bubble)
A virtual environment isolates your project dependencies. It's like a "bubble" where you install only what H2Ops needs.
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step B: Installing the "Engine" (Requirements)
We install all libraries listed in `requirements.txt`.
```powershell
pip install -r requirements.txt
```

### Step C: The Heart (The Database)
1. Open **XAMPP Control Panel**.
2. Start **Apache** and **MySQL**.
3. Go to `http://localhost/phpmyadmin/` and create a database named `h2ops_db`.

### Step D: First Pulse (Migration)
We need to create the tables (Branch, User, Product, etc.) and seed initial data.
```powershell
python migrate_db.py
```

---

## 4. Verification: Is it Alive?
Once setup is complete, run:
```powershell
python app.py
```
Visit `http://127.0.0.1:5000` in your browser. If you see the login screen, **Congratulations!** You have completed Lesson 1.

---

## ✍️ Practice Task
1. **Explore the Files:** Open `models.py` and see if you can find where the `Branch` and `User` tables are defined.
2. **Check the DB:** Go to `phpmyadmin` and look inside `h2ops_db`. Can you see the tables that were created?

> [!TIP]
> Always keep your virtual environment activated when working on the project. You'll know it's active if you see `(venv)` in your terminal.

---
**Next Up:** *Lesson 2: Flask Basics & Project Architecture*
