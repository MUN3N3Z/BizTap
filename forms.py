"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import RadioField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

class InventoryForm(FlaskForm):
        # Data to be collected and displayed on inventory page
        stock_name = StringField("Name")
        stock_unit = StringField("Available Units", [DataRequired()])
        stock_lowest = StringField("Lowest limit", [DataRequired()])
        submit = SubmitField('Submit')

class AccountingForm(FlaskForm):
        # Data fields to be displayed
        expenses = IntegerField("Expenses", [DataRequired()])
        revenue = IntegerField("Revenue", [DataRequired()])
        sales = IntegerField("Sales", [DataRequired()])
        assets = IntegerField("Assets", [DataRequired()]) 
        liabilities = IntegerField("Liabilities", [DataRequired()])
        inventory = IntegerField("Inventory", [DataRequired()])
        submit = SubmitField('Submit')

class EmployeesForm(FlaskForm):
        # Data fields to be displayed
        name = StringField("Name", [DataRequired()])
        age = IntegerField("Age", [DataRequired()])
        salary = IntegerField("Salary", [DataRequired()])
        hours = IntegerField("Working Hours/Week", [DataRequired()])
        id_number = IntegerField("ID Number", [DataRequired()])
        days = RadioField("Off Day", choices=[("Sunday", "Sunday"), ("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thurday"), ("Friday", "Friday"), ("Saturday", "Saturday")])
        submit = SubmitField('Submit')
