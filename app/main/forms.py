from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional


class SearchForm(FlaskForm):
    q = StringField("Search", validators=[Optional()])
    submit = SubmitField("Search")