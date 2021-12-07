"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class InventoryForm(FlaskForm):
        # Data to be collected and displayed on inventory page
        stock_name = StringField("Name")
        stock_unit = StringField("Available Units", [DataRequired()])
        stock_lowest = StringField("Lowest limit", [DataRequired()])
        submit = SubmitField('Submit')

class AccountingForm(FlaskForm):
        # Data fields to be displayed
        expenditure = StringField("Expenditure", [DataRequired()])
        revenue = StringField("Revenue", [DataRequired()])
