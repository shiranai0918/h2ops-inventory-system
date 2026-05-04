# Lesson 4: Routes — The Road Map of Your System 🗺️

In Lesson 2, we learned that Blueprints are like "mini-apps." In this lesson, we will learn how to build the actual **Routes** that make your system interactive.

---

## 1. What is a Route?
A route is simply a path. For example:
- `http://localhost:5000/sales/` -> Shows the list of sales.
- `http://localhost:5000/sales/create` -> Shows the form to add a new sale.

In Python, we define these using **Decorators** (the lines starting with `@`).

---

## 2. GET vs POST (The Conversation) 🗣️
Most routes use two "methods" to talk to the browser:
- **GET:** The browser asks: *"Please give me the page (the HTML)."*
- **POST:** The browser says: *"Here is some data the user typed into a form. Please save it!"*

Look at **[routes/sales.py](file:///c:/Projects/Capstone%20System/routes/sales.py)** (Line 19):
```python
@sales_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # ... logic to save the sale ...
    return render_template('sales/create.html')
```

---

## 3. Passing Data to the Template 🎁
When you want to show data from your database (like a list of Products) on your website, you "pass" it to the template:

```python
products = Product.query.all()
return render_template('sales/create.html', products=products)
```
- **`products` (on the left):** This is what the HTML file will call it.
- **`products` (on the right):** This is the Python variable containing the data.

---

## 4. The URL Builder (`url_for`) 🔗
Instead of typing `href="/sales/create"`, we use a special function called `url_for('sales.create')`.

**Why?**
If you ever decide to change the address from `/sales/create` to `/sales/new-order`, you don't have to update 100 HTML files. `url_for` will automatically find the new address for you!

---

## ✍️ Practice Task
1. **Trace the Logic:** Open **[routes/sales.py](file:///c:/Projects/Capstone%20System/routes/sales.py)** and look at the `create()` function (Line 21). 
2. **Find the Redirect:** After a sale is successfully recorded (Line 83), where does the system send the user? (Look for the `redirect(url_for(...))` line).
3. **The "Flash" Message:** Find the `flash()` line. What message will the user see on their screen after they successfully add a sale?

---
**Next Up:** *Lesson 5: Templates & Jinja2 — The Visual Interface*
