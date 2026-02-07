"""
Demo Flask Application - Intentionally contains issues for AI Code Review
This app has security vulnerabilities, code smells, and performance issues
"""

from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# ISSUE 1: Hardcoded credentials (Security vulnerability)
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"


# ISSUE 2: SQL Injection vulnerability
@app.route("/user/<username>")
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    return str(result)


# ISSUE 3: No input validation
@app.route("/calculate", methods=["POST"])
def calculate():
    num1 = request.form.get("num1")
    num2 = request.form.get("num2")
    # No type checking or validation
    result = int(num1) / int(num2)  # Potential division by zero
    return f"Result: {result}"


# ISSUE 4: XSS vulnerability
@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    # Direct HTML rendering without escaping
    return render_template_string(f"<h1>Hello {name}!</h1>")


# ISSUE 5: Inefficient code - N+1 query problem
@app.route("/orders")
def get_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    orders = cursor.execute("SELECT id FROM orders").fetchall()
    result = []
    for order in orders:
        # Multiple queries in a loop - inefficient
        details = cursor.execute(
            f"SELECT * FROM order_details WHERE order_id = {order[0]}"
        ).fetchall()
        result.append(details)
    return str(result)


# ISSUE 6: Missing error handling
@app.route("/file/<filename>")
def read_file(filename):
    # Path traversal vulnerability + no error handling
    with open(f"/data/{filename}") as f:
        content = f.read()
    return content


# ISSUE 7: Unused imports and variables
import json
import datetime

unused_variable = "This is never used"

if __name__ == "__main__":
    # ISSUE 8: Debug mode in production
    app.run(debug=True, host="0.0.0.0", port=5000)
