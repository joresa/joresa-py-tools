from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

class DiffForm(FlaskForm):
    text1_name = StringField('Text 1 Name', default='Text 1')
    text1 = TextAreaField('Text 1', validators=[DataRequired()])
    text2_name = StringField('Text 2 Name', default='Text 2')
    text2 = TextAreaField('Text 2', validators=[DataRequired()])
    submit = SubmitField('Compare')

class RuleCardForm(FlaskForm):
    input_text = TextAreaField('Rule card text', validators=[DataRequired()])
    format_type = RadioField('Format', choices=[
        ('bulleted', 'Bulleted format'),
        ('hierarchical', 'Hierarchical format'),
        ('jira_html', 'Jira HTML (IDs bold)')
    ], default='bulleted')
    submit = SubmitField('Format')
