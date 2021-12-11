import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from forms import InventoryForm, AccountingForm
from cs50 import SQL


# Configure application
app = Flask(__name__)

# Set Secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


# Configure users database
db = SQL("sqlite:///users.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Default homepage
@app.route("/")
@login_required
def index():
        
        # Identify current user
        id = session["user_id"]

        return render_template("index.html")
    
@app.route("/login", methods = ["POST", "GET"])
def login():
        """Log user in"""

        # Forget any user_id
        session.clear()

        if request.method == "POST":
                
                # Ensure username was submitted
                if not request.form.get("username"):
                        return apology("must provide username", 400)

                # Ensure password was submitted
                elif not request.form.get("password"):
                        return apology("must provide password", 400)
                
                # Query database for username
                rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
                
                # Ensure username exists and password is correct
                if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                        return apology("invalid username and/or password", 400)

                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]

                # Redirect user to home page
                return redirect("/")
        # User reached route via GET
        else:
                return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
        """Register user"""
        # User reached route via GET
        if request.method == "GET":

                # Redirect user to registration page
                return render_template("register.html")
        else:
                # Check for errors
                if not request.form.get("username"):
                        return apology("must provide username", 400)
                elif not request.form.get("password"):
                        return apology("must provide password", 400)
                elif not request.form.get("confirmation"):
                        return apology("must provide confirmation password", 400)

                # Check if confirmation password matches passsword
                elif request.form.get("password") != request.form.get("confirmation"):
                        return apology("Confirmation password must match initial password", 400)

                # Query database for usernames
                rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

                # Check if username already exists
                if len(rows) != 0:
                        return apology("Username exists", 400)
                
                # Hash user's password
                hash = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)

                # Add user to database
                db.execute("INSERT INTO users (username, hash, email) values(?, ?, ?)", request.form.get("username"), hash, request.form.get("email"))

                # Query database for usernames
                rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
                
                # Log user in
                session["user_id"] = rows[0]["id"]

                # Redirect user to home page
                return redirect("/") 

# Configure inventory database
db_inventory = SQL("sqlite:///inventory.db")

@app.route('/inventory', methods=["GET", "POST"])
@login_required
def inventory():
        return render_template("inventory.html")

        
@app.route('/inventoryform', methods=["GET", "POST"])
@login_required
def inventoryform():

        # Get form object
        form = InventoryForm()
        if form.validate_on_submit():

                 # Get data from the form
                name = form.stock_name.data
                units = form.stock_unit.data
                limit = form.stock_lowest.data
                
                 # Get data from inventory page
                rows = db_inventory.execute("SELECT * FROM inventory WHERE name = ?", name)

                 # Get user ID
                id = session["user_id"]

                 # Check whether stock exits and update inventory table with data
                 # Stock doesn't exist
                if rows:
                
                         # Update existing row
                        db_inventory.execute("UPDATE inventory SET units = ?, lower_limit = ? WHERE name = ?",units, limit, name )
                
                 # Stock already exists
                else:
                        
                         # Update inventory database with new data
                        db_inventory.execute("INSERT INTO inventory (name, units, lower_limit, user_id) VALUES (?, ?, ?, ?)", name, units, limit, id)

                return render_template("inventory.html")

        # Request method is "Get"
        return render_template("inventoryform.html", form=form)



@app.route("/inventorytable", methods=["GET", "POST"])
@login_required
def inventorytable():

        # Get user ID
        id = session["user_id"]

        # Get data from database
        rows = db_inventory.execute("SELECT * FROM inventory WHERE user_id = ? ORDER by time DESC", id)
        return render_template("inventorytable.html", rows=rows)


@app.route("/accounting", methods=["GET", "POST"])
@login_required
def accounting():

        return render_template("accounting.html")

@app.route("/accountingform", methods=["GET", "POST"])
@login_required
def accountingform():

        # Get the Accounting form 
        form = AccountingForm()

        if form.validate_on_submit():

                print("ok1")

                # Get data from the form
                revenue = form.revenue.data
                expenses = form.expenses.data
                sales = form.sales.data
                assets = form.assets.data
                liabilities = form.liabilities.data
                inventory = form.inventory.data

                # Get user ID
                id = session["user_id"]

                # Get data from inventory page
                rows = db_inventory.execute("SELECT * FROM accounting WHERE user_id = ?", id)
                print("ok2")

                # If user already exists in accounting table
                if rows:

                        # Update existing row
                        db_inventory.execute("UPDATE accounting SET revenue = ?, expenses = ?, sales = ?, assets = ?, liabilities = ?, inventory = ? WHERE id = ?",revenue, expenses, sales, assets, liabilities, inventory, id)
                        print("ok3")

                
                # User does not exists
                else: 

                        # Update inventory database with new data
                        db_inventory.execute("INSERT INTO accounting (revenue, expenses, sales, assets, liabilities, inventory) VALUES (?, ?, ?, ?, ?, ?)", revenue, expenses, sales, assets, liabilities, inventory)
                        print("ok4")

                return render_template("accounting.html")

        # Request method is "Get"
        return render_template("accountingform.html", form=form) 


@app.route("/accountingtable", methods=["GET", "POST"])
@login_required
def accountingtable():

        # Get the Accounting form 
        form = AccountingForm()

        # Get user ID
        id = session["user_id"]

        # Get data from database
        rows = db_inventory.execute("SELECT * FROM accounting WHERE user_id = ?", id)

        # Check if user has accounting data
        # User is present
        if rows:
                # Get data from rows
                revenue = rows[0]["revenue"]
                expenses = rows[0]["expenses"]
                sales = rows[0]["sales"]
                assets = rows[0]["assets"]
                liabilities = rows[0]["liabilities"]
                inventory = rows[0]["inventory"]

                # Calculate accounting data
                current_ratio = (assets / liabilities)
                net_income = (revenue - expenses)
                quick_ratio = ((assets - inventory) / liabilities)
                profit = (revenue - expenses)

                # Display table with user's accounting data
                return render_template("accountingtable.html", current_ratio=current_ratio, net_income=net_income, quick_ratio=quick_ratio, profit=profit)

        # User data not found
        else:

                return render_template("accountingform.html", form=form)

                

@app.route("/employees", methods=["GET", "POST"])
@login_required
def employees():
        return render_template("employees.html")

@app.route("/socials", methods=["GET", "POST"])
@login_required
def socials():
        return render_template("socials.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
