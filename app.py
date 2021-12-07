import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.helpers import url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from forms import InventoryForm

# Configure application
app = Flask(__name__, instance_relative_config=False)


# Set secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Configure users database
db = SQL("sqlite:///users.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
def inventory():

        # Get form object
        form = InventoryForm()

        render_template('inventory.html', form=form)

        if form.validate_on_submit() and request.method == "POST":

                # Get data from the form
                name = form.stock_name.data
                units = form.stock_unit.data
                limit = form.stock_unit.data
                
                # Get data from inventory page
                rows = db_inventory.execute("SELECT * FROM inventory WHERE name = ?", name)

                # Check whether stock exits and update inventory table with data
                # Doesn't exist
                if not name == rows[0][" name"]:

                        # Update inventory database with new data
                        db_inventory.execute("INSERT INTO inventory (name, units, lower_limit) VALUES (?, ?, ?)", name, units, limit)
                
                # Stock already exists
                else:
                        # Update existing row
                        db_inventory.execute("UPDATE inventory SET units = ?, limit = ? WHERE name = ?",units, limit, name )
                
                return render_template("inventory.html", form=form)

        else:
                return render_template("inventory.html", form=form)
        



@app.route("/accounting", methods=["GET", "POST"])
@login_required
def accounting():
        return render_template("accounting.html")


        # if request.method == 'POST' and form.validate():
                
        #         # Obtain data fields from the form
        #         name = form.stock_name.data
        #         units = form.stock_unit.data
        #         limit = form.stock_lowest.data

        #         # Render template with Inventory table
        #         return render_template("inventory.html", name=name, units=units, limit=limit)
        # else:

        #         return render_template("inventory.html")

@app.route("/employees", methods=["GET", "POST"])
@login_required
def employees():
        return render_template("employees.html")

@app.route("/socials", methods=["GET", "POST"])
@login_required
def socials():
        return render_template("socials.html")

