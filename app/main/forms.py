from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    q = StringField("Search", validators=[Length(max=64)])
    submit = SubmitField("Search")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=140)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish")