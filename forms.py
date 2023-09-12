from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, validators
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
    firstname = StringField("First Name: ", validators=[DataRequired()], render_kw={"placeholder": "Enter first Name"})
    lastname = StringField("Last Name: ", validators=[DataRequired()], render_kw={"placeholder": "Enter last Name"})
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), validators.EqualTo('password_confirm',
                                                                                          message="Passwords doesn't must match")])
    password_confirm = PasswordField("Confirm_Password: ", validators=[DataRequired()])
    sign_up = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField("Password: ", validators=[DataRequired()], render_kw={"placeholder": "password"})
    sign_in = SubmitField("Sign In")


class BookDetailsForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired()], render_kw={"placeholder": "Title"})
    subtitle = StringField("SubTitle: ", validators=[DataRequired()], render_kw={"placeholder": "Subtitle"})
    author = StringField("Author: ", validators=[DataRequired()], render_kw={"placeholder": "Author"})
    brand_name = StringField("Publisher: ", validators=[DataRequired()], render_kw={"placeholder": "Publisher_name:"})
    number_of_pages = StringField("Number_of_pages: ", validators=[DataRequired()],
                                  render_kw={"placeholder": "Number_of_pages"})
    book_contains = StringField("Book_contains: ", validators=[DataRequired()],
                                render_kw={"placeholder": "Book_contains"})
    isbn = StringField("ISBN: ", validators=[DataRequired()], render_kw={"placeholder": "isbn"})
    no_of_copies = StringField("no_of_copies: ", validators=[DataRequired()])
    image = FileField("Upload Image: ", validators=[FileRequired(),
                                                    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')],
                      render_kw={"placeholder": "'jpg', 'png', 'jpeg'"})
    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    review_text = CKEditorField("Book Review:", validators=[DataRequired()])
    submit = SubmitField("Submit Review")


class UserRoleForm(FlaskForm):
    user_role = StringField("Role", validators=[DataRequired()])
    description=StringField("Role", validators=[DataRequired()])
