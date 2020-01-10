from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

#DEGREE FORMS PAGE 
class DegreeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    domain = StringField('Domain', validators=[DataRequired()])
