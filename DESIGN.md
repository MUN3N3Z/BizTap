BizTap is conceptually divided in the following sections:

## Login/Registration
This section enables a user to log into the website using a password and username, which are stored in an SQLlite table. The passwords are hashed before being entered into the table to increase security. I used html forms to render the login form, together with Python and SQL queries to authenticate the user before log in.

In the event of a new user, a user is required to fill out a HTML form, with their username, password, confirmation password (same as password), and unique email, each of which are stored in a users SQLite table

## Homepage
This is the landing page, which primarily relies on a HTML template. It contains buttons with hyper-references to all the primary functionalities of the app - inventory, accounting, employee management, logout.

## Inventory
The inventory button renders a html landing page through the /inventory route in app.py. The landing page incorporates HTML, JavaScript and CSS to make it responsive. It contains two functional buttons which render the inventory form and inventory table respectively.

The invetory form page makes use of FlaskForms, where a user fills out the name, quantity and minimum limit of the item in the invetory. This information is then stored in an SQL Table

The inventory table page retrieves data from the invetory table and renders the information in a HTML table.

## Accounting
The invetory button renders a html landing page through the /accounting route. The landing page too, similar to the inventory one, incorporates HTML, JavaScript and CSS for responsiveness.

The accounting form uses a FlaskForm to collect accounting data the user, which is then passed through accounting equations (using Python) in the /accountingtable route and rendered in a HTML table using Jinja.

Furthermore this page links another html page where a user can learn a couple of simple accounting formulas.
## Employees
The employees landing page comprises HTML, JavaScript and CSS for responsiveness. The two routes incorporated in the page: /employeesform and /employees table use FlaskForms to collect employee data form the user and display it in a schedule table. Ideally, the table was supposed to schedule employees on their respective working days, but I did not manage to implement that.

## Logout
This function clears the user's session in the app using Flask's session object.