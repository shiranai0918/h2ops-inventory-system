# Lesson 2: Flask Basics & Project Architecture 🏗️

In Lesson 1, we set up the environment. Now, let's look under the hood. How does a single Python file turn into a professional web application with multiple pages?

---

## 1. The "Traffic Controller" (Routes)
In Flask, a **Route** is a connection between a URL (like `/dashboard`) and a Python function. 

When you visit `http://localhost:5000/auth/login`, Flask does this:
1. It looks at the URL.
2. it finds the function assigned to `/auth/login`.
3. It runs that function and sends back the HTML result.

---

## 2. The Application Factory (`app.py`)
Open your **[app.py](file:///c:/Projects/Capstone%20System/app.py)** file. You will see a function called `create_app()`. 

This is the "Brain" of the system. It:
- **Configures the App:** Connects the database and sets security keys.
- **Initializes Extensions:** Sets up the login system (`login_manager`) and encryption (`bcrypt`).
- **Registers Blueprints:** This is the most important part of our architecture.

---

## 3. Modular Architecture (Blueprints) 🧩
Instead of putting 1,000 lines of code in one file, we use **Blueprints**. We split the system into smaller "mini-apps":

| Blueprint | Folder Location | Responsibility |
| :--- | :--- | :--- |
| **Auth** | `routes/auth.py` | Login, Logout, Password Resets. |
| **Sales** | `routes/sales.py` | Recording sales and transactions. |
| **Inventory** | `routes/inventory.py` | Tracking stock levels of water and caps. |
| **Reports** | `routes/reports.py` | Sales analytics and forecasting. |

### Why Blueprints?
Imagine if 3 group members wanted to work at the same time. 
- Member A works on `auth.py`.
- Member B works on `sales.py`.
- Member C works on `inventory.py`.
Because they are separate files, you won't have "merge conflicts" or overwrite each other's work!

---

## 4. The Request Cycle
Here is how data flows through H2Ops:
1. **User** clicks a button in the browser (HTML).
2. **Flask** finds the correct Blueprint and Function (Route).
3. **The Function** asks the **Database** for data (Models).
4. **The Function** sends that data to a **Template** (HTML/Jinja2).
5. **The User** sees the updated page.

---

## ✍️ Practice Task
1. **Find a Route:** Open **[routes/auth.py](file:///c:/Projects/Capstone%20System/routes/auth.py)**. Can you find the `@auth_bp.route('/login')` line?
2. **Trace the Template:** Look at the return statement of that login function. Which HTML file is it opening? (Hint: look in the `templates/` folder).

> [!IMPORTANT]
> Understanding Blueprints is the key to being a professional developer. It’s what separates a "small script" from a "scaleable system."

---
**Next Up:** *Lesson 3: Database Design — The Foundation of Everything*
