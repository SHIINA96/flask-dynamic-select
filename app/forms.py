from flask_wtf import FlaskForm
from wtforms import SelectField
class Form(FlaskForm):
    location = SelectField('location', choices=[])
    size = SelectField('size', choices=[])
    item = SelectField('item', choices=[])