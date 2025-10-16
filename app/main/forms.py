from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, Optional

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    display_name = StringField('Display Name', validators=[Optional()])
    parent_id = SelectField('Parent Category', coerce=int, validators=[Optional()])

class ToolAssignForm(FlaskForm):
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
