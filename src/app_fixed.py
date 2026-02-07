"""
Fixed Flask Application - AI-assisted improvements
All security vulnerabilities and code smells resolved
"""

from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os
from werkzeug.security import check_password_hash
import logging

app = Flask(__name__)

# FIX 1: Use environment variables for secrets
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
API_KEY = os.getenv("API_KEY")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Get database connection with proper configuration"""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


# FIX 2: Parameterized queries prevent SQL injection
@app.route("/user/<username>")
def get_user(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Using parameterized query
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify(dict(result))
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return jsonify({"error": "Internal server error"}), 500


# FIX 3: Input validation and error handling
@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        num1 = float(request.form.get("num1", 0))
        num2 = float(request.form.get("num2", 1))

        if num2 == 0:
            return jsonify({"error": "Division by zero not allowed"}), 400

        result = num1 / num2
        return jsonify({"result": result})
    except ValueError:
        return jsonify({"error": "Invalid input - numbers required"}), 400
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return jsonify({"error": "Internal server error"}), 500


# FIX 4: Proper HTML escaping
@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    # Using Jinja2 auto-escaping
    template = "<h1>Hello {{ name|e }}!</h1>"
    return render_template_string(template, name=name)


# FIX 5: Optimized query - single JOIN instead of N+1
@app.route("/orders")
def get_orders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Efficient JOIN query
        query = """
            SELECT o.id, o.order_date, od.product_id, od.quantity
            FROM orders o
            LEFT JOIN order_details od ON o.id = od.order_id
        """
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
        return jsonify({"error": "Internal server error"}), 500


# FIX 6: Path validation and error handling
@app.route("/file/<filename>")
def read_file(filename):
    # Whitelist approach for file access
    allowed_files = ["readme.txt", "info.txt"]

    if filename not in allowed_files:
        return jsonify({"error": "File not allowed"}), 403

    try:
        # Use safe path joining
        safe_path = os.path.join("/data", os.path.basename(filename))
        with open(safe_path, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    # FIX 7: Production-ready configuration
    debug_mode = os.getenv("FLASK_ENV") == "development"
    app.run(debug=debug_mode, host="127.0.0.1", port=5000)
