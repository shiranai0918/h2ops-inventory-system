# 🚀 Capstone System Installation Guide

This guide will walk you through setting up and running the Capstone System on your local Windows machine using Visual Studio Code (VS Code).

### 🛠️ Step 1: Install Prerequisites
Before you begin, ensure you have the following installed on your laptop:
1. **VS Code**: If you haven't already, download and install it from [code.visualstudio.com](https://code.visualstudio.com/).
2. **Python**: Download and install the latest version from [python.org](https://www.python.org/downloads/). **Important:** During installation, make sure to check the box that says **"Add Python to PATH"**.
3. **XAMPP**: Since this project uses a MySQL database, download and install XAMPP from [apachefriends.org](https://www.apachefriends.org/index.html).

### 🗄️ Step 2: Set Up the Database
1. Open the **XAMPP Control Panel**.
2. Click the **Start** button next to **Apache** and **MySQL**. (Wait for both of them to turn green).
3. Open your web browser and go to: `http://localhost/phpmyadmin`
4. On the left sidebar, click on **New**.
5. In the "Database name" field, type exactly: **`h2ops_db`**
6. Click **Create**. *(You do not need to add any tables manually; the code will do this for you).* # Export mo nalang ney ang database nga gin send ko

### 📂 Step 3: Open the Project in VS Code
1. Download the project folder from Google Drive and **Extract/Unzip** it to a location on your computer (e.g., your Desktop or Documents).
2. Open **VS Code**.
3. Go to **File > Open Folder...** and select the extracted project folder (the one containing `app.py`).
4. In VS Code, open a new terminal by clicking **Terminal > New Terminal** from the top menu. (Ensure the terminal is a PowerShell or Command Prompt).

### 🐍 Step 4: Set Up the Python Environment
In the VS Code terminal, run the following commands one by one:

**1. Create a virtual environment** (This keeps the project's packages separate from your main system):
```bash
python -m venv venv
```

**2. Activate the virtual environment**:
```bash
.\venv\Scripts\activate
```
*(Note: If you get a "running scripts is disabled" error, run this command first: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`, then try activating again. You should see `(venv)` appear at the beginning of your terminal line).*

**3. Install project requirements**:
```bash
pip install -r requirements.txt
```
*(Wait for all the downloads and installations to finish).*

### 🌱 Step 5: Initialize the Database
Now that your database is created in XAMPP, we need to add the tables and the default users. In the terminal, run:
```bash
python seed.py
```
*(You should see a message saying "Database seeded successfully" indicating that the admin and staff accounts have been created).*

### 🚀 Step 6: Run the Application
Finally, start the web server by running:
```bash
python app.py
```
*(Or `flask run` if it's preferred).*

**Access the System:**
Once the server is running, open your web browser and go to:
👉 **`http://localhost:5000`**

### 🔑 Default Login Credentials
You can use the following default accounts created by the seed script to log in:

**Admin Account:**
- **Username:** `admin`
- **Password:** `password123`

**Staff Account (Tagbak Branch):**
- **Username:** `staff_tagbak`
- **Password:** `password123`

---
*To stop the server at any time, go to the VS Code terminal and press `Ctrl + C`.*
