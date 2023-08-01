from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField,validators
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()], render_kw={"placeholder":"Enter full Name"})
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), validators.EqualTo('password_confirm', message="Passwords doesn't must match")])
    password_confirm = PasswordField("Confirm_Password: ", validators=[DataRequired()])
    sign_up = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()],render_kw={"placeholder": "Enter your email"})
    password = PasswordField("Password: ", validators=[DataRequired()],render_kw={"placeholder": "password"})
    sign_in = SubmitField("Sign In")


class BookdetailsForm(FlaskForm):
    title = StringField("Book Name: ", validators=[DataRequired()],render_kw={"placeholder": "Title"} )
    author = StringField("Author Name: ", validators=[DataRequired()],render_kw={"placeholder": "Author"})
    no_of_copies = StringField("no_of_copies: ", validators=[DataRequired()])
    image = FileField("Upload Image: ", validators=[FileRequired(),
                                                    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')],render_kw={"placeholder": "'jpg', 'png', 'jpeg'"})
    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    review_text = CKEditorField("Book Review:", validators=[DataRequired()])
    submit = SubmitField("Submit Review")
