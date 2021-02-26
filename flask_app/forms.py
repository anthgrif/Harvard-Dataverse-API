from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Form to query by ID
class QueryByIDForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    submit1 = SubmitField('Search by ID')

# Form to query by specific field
class QueryByFieldForm(FlaskForm):
    field = StringField('field', validators=[DataRequired()])
    val = StringField('value', validators=[DataRequired()])
    submit2 = SubmitField('Search by field')
