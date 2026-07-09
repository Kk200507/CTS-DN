"""
Flask Framework Demonstration.

This is a self-contained, runnable Flask application demonstrating fundamental 
concepts including routing, dynamic parameters, blueprints, template rendering,
database models via SQLAlchemy, and error handling.

To run this application:
  1. Install dependencies: pip install Flask Flask-SQLAlchemy
  2. Execute the script: python flask_demo.py
  3. Open your browser and navigate to http://127.0.0.1:5000/
"""

from flask import Flask, request, jsonify, render_template_string, Blueprint, abort
from flask_sqlalchemy import SQLAlchemy

# ==============================================================================
# 1. APPLICATION SETUP & CONFIGURATION
# ==============================================================================

app = Flask(__name__)

# Configure an in-memory SQLite database for testing and demonstration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)


# ==============================================================================
# 2. DATABASE MODEL (SQLAlchemy)
# ==============================================================================

class Product(db.Model):
    """
    SQLAlchemy Model representing a Product in our store.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        """Helper method to convert model into a dictionary for JSON responses."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description
        }


# Create database tables and populate mock data for demo purposes
with app.app_context():
    db.create_all()
    # Add dummy products
    db.session.add(Product(name="Python mug", price=12.99, description="Best coffee mug for developers"))
    db.session.add(Product(name="Mechanical Keyboard", price=99.99, description="Clicky switches"))
    db.session.commit()


# ==============================================================================
# 3. ROUTES & URL PARAMETERS
# ==============================================================================

@app.route("/")
def home():
    """
    Simple static route matching GET /
    """
    return jsonify({
        "message": "Welcome to the Flask Demo API!",
        "endpoints_available": [
            "/products (GET, POST)",
            "/products/<id> (GET)",
            "/render-demo (GET)",
            "/admin/dashboard (GET - Blueprint demo)",
            "/cause-error (GET - Error handler demo)"
        ]
    })


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Dynamic route demonstrating path parameters.
    `<int:product_id>` matches integers only and passes it as an argument.
    """
    # Fetch the product from database
    product = Product.query.get(product_id)
    if not product:
        abort(404, description=f"Product with ID {product_id} was not found.")
    
    return jsonify(product.to_dict())


# ==============================================================================
# 4. REQUEST METHODS (GET & POST)
# ==============================================================================

@app.route("/products", methods=["GET", "POST"])
def manage_products():
    """
    Route demonstrating handling multiple HTTP methods.
    - GET: Retrieves a list of all products.
    - POST: Reads JSON body parameters to insert a new product.
    """
    if request.method == "POST":
        # Extract json payload
        data = request.get_json()
        
        # Simple validation
        if not data or "name" not in data or "price" not in data:
            return jsonify({"error": "Missing 'name' or 'price' fields"}), 400
        
        # Instantiate and save model
        new_product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description", "")
        )
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify(new_product.to_dict()), 201
        
    else:  # GET method
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])


# ==============================================================================
# 5. JINJA2 TEMPLATE RENDERING
# ==============================================================================

@app.route("/render-demo")
def render_demo():
    """
    Demonstrates Jinja2 templates using render_template_string to keep it self-contained.
    Shows variables, loops, and conditions.
    """
    products = Product.query.all()
    
    # Inline HTML template demonstrating Jinja2 syntax logic
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jinja2 Template Demo</title>
        <style>
            body { font-family: sans-serif; margin: 40px; background-color: #f4f6f9; }
            h1 { color: #333; }
            .card { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .expensive { border-left: 5px solid red; }
            .cheap { border-left: 5px solid green; }
        </style>
    </head>
    <body>
        <h1>Store Products</h1>
        <p>This page is dynamically rendered on the server side using the Jinja2 engine.</p>
        
        {% if products %}
            <div>
                {% for item in products %}
                    <!-- Conditional styling classes based on price -->
                    <div class="card {% if item.price > 50 %}expensive{% else %}cheap{% endif %}">
                        <h3>{{ item.name | upper }}</h3>
                        <p>Price: <strong>${{ item.price }}</strong></p>
                        <p>{{ item.description }}</p>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <p>No products available in database.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(template, products=products)


# ==============================================================================
# 6. BLUEPRINT MODULE
# ==============================================================================

# Blueprints allow you to organize your code into modular components.
# Here we define an admin blueprint with prefix `/admin`.
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
def admin_dashboard():
    """
    Sub-route mapping to /admin/dashboard.
    """
    return jsonify({
        "status": "success",
        "role": "administrator",
        "message": "Welcome to the Administration Console Dashboard."
    })

# Register the Blueprint with the main application
app.register_blueprint(admin_bp)


# ==============================================================================
# 7. CUSTOM ERROR HANDLING
# ==============================================================================

@app.errorhandler(404)
def resource_not_found(error):
    """
    Custom global handler for HTTP 404 Not Found errors.
    Returns custom JSON instead of default Flask HTML error pages.
    """
    return jsonify({
        "error": "Not Found",
        "message": error.description or "The requested URL was not found on this server."
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Custom global handler for HTTP 500 Internal Server errors.
    """
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred. Please try again later."
    }), 500


@app.route("/cause-error")
def cause_error():
    """
    Route that throws a division-by-zero exception to test HTTP 500 handler.
    """
    return 1 / 0


# ==============================================================================
# EXECUTION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # Start the local development server in debug mode
    # debug=True enables auto-reloading and helpful traceback logs
    app.run(debug=True)
