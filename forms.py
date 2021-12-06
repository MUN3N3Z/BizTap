"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class InventoryForm(FlaskForm):
        # Data to be collected and displayed on inventory page
        stock_name = StringField("Name", [Length(min=4, max=25)])
        stock_unit = StringField("Available Units", [DataRequired()])
        stock_lowest = StringField("Lowest limit", [DataRequired()])
        submit = SubmitField('Submit')