from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed

class SearchForm(FlaskForm):
    q = StringField("Search", validators=[Length(max=64)])
    submit = SubmitField("Search")

class CommentForm(FlaskForm):
    body = TextAreaField("Comment", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Post Comment")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=140)])
    content = TextAreaField("Content", validators=[DataRequired()])
    image = FileField("Image", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"])])
    submit = SubmitField("Publish")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField("Send")