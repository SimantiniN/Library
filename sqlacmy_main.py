import datetime as dt
from bs4 import BeautifulSoup


from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import aliased, sessionmaker
from flask_login import LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, BookDetailsForm, ReviewForm
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_gravatar import Gravatar
from flask import abort
from functools import wraps

# import all files from python_files folder
from library.python_files.Database_tables import User, Book_Copies, Book, Book_Status, Book_Review
from library.python_files.book_DML_operations import Add_Book_To_DB
from library.python_files.register_login import Registration
from library.python_files.book_reserve_renew import Reserve_operations
from library.python_files.withdraw_return import Dereserve_returns
from library.python_files.book_approval import Approve_books, reserve_books_count
from library.python_files.reports import Reports
from library.python_files.loan import Loan_Details
from library.python_files.bookreview import Review

app = Flask(__name__)
app.config['SECRET_KEY'] = "h6a6r1h3a27r8386ma99ha1d3va"
app.config['SECURITY_PASSWORD_SALT'] = "Omnamhashivay"
bootstrap = Bootstrap(app)
ckeditor = CKEditor(app)
bcrypt = Bcrypt(app)

# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_mail_username'
app.config['MAIL_PASSWORD'] = 'your_mail_password'

# CONNECT TO DB
engine = create_engine('sqlite:///Librarysqlachmy.db')
Session = sessionmaker(bind=engine)
session = Session()

# upload the image /file
UPLOAD_FOLDER = './static/books'  # where to store uploaded files
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# gravator
gravatar = Gravatar(app, size=35, rating='g', default='robohash', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)

# login Authentication
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


# admin permission
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1 or not current_user.is_authenticated:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


# functions to upload image
@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    total_reserve_books = 0
    current_date = dt.datetime.today().strftime("%B %d,%Y")
    book_data = session.query(Book).all()

    # total_book_copies = session.query(Book_Copies).all()

    if not book_data:
        flash("Contact Admin no books are currently available.")
    if current_user.is_authenticated:
        total_reserve_books = reserve_books_count(current_user.id, session)

    return render_template("index.html", date=current_date, books=book_data, reserve_books_count=total_reserve_books,
                           logged_in=current_user.is_authenticated)  # , total_books_on_loan=loans)


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    registration_form = RegisterForm()
    if registration_form.validate_on_submit():
        register = Registration(session, app)
        is_exists = register.user_registration(registration_form)
        if is_exists:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        return redirect(url_for("login"))
    return render_template("registration.html", form=registration_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        userlogin = Registration(session, app)
        is_login = userlogin.user_login(login_form)
        if is_login:
            return redirect(url_for('home'))
        else:
            flash("Username or Password incorrect!Please try again.")
    return render_template('login.html', form=login_form, logged_in=current_user.is_authenticated)


@app.route('/add_book', methods=['GET', 'POST'])
@admin_only
@login_required
def add_book():
    return render_template('add_book.html')


@login_required
@admin_only
@app.route('/add_book_details', methods=['GET', 'POST'])
def add_book_details():
    book_form = BookDetailsForm()
    if book_form.validate_on_submit():
        book_to_add = Add_Book_To_DB(session, app)
        is_success = book_to_add.add_book_to_db(book_form)
        flash(is_success)
        # else:
        #     flash('Failed to add the book')
        return redirect(url_for('home'))
    return render_template('add_book_details.html', form=book_form, logged_in=current_user.is_authenticated)


@app.route("/edit_book/<int:book_id>", methods=['GET', 'POST'])
@login_required
@admin_only
def edit_book(book_id):
    book_to_edit = session.query(Book).get(book_id)
    if book_to_edit is None:
        return "Book not found", 404
    edit_form = BookDetailsForm(

        title=book_to_edit.title,
        sub_title=book_to_edit.sub_title,
        author=book_to_edit.author,
        brand_name=book_to_edit.brand_name,
        number_of_pages=book_to_edit.number_of_pages,
        book_contains=book_to_edit.book_contains,
        isbn=book_to_edit.isbn,
        no_of_copies=book_to_edit.no_of_copies

    )
    if edit_form.validate_on_submit():
        book_to_add = Add_Book_To_DB(session, app)
        is_success = book_to_add.add_book_to_db(edit_form)
        if is_success:
            return redirect(url_for('home'))
        else:
            return "Failed to Edit"
    return render_template('add_book_details.html', form=edit_form, is_edit=True,
                           current_user=current_user.is_authenticated, logged_in=True)


@app.route("/delete/<int:book_id>")
@login_required
@admin_only
def delete_book(book_id):
    book_to_del = Add_Book_To_DB(session, app)
    is_delete = book_to_del.deletion_of_book(book_id)
    flash(is_delete)
    return redirect(url_for('home'))


@app.route("/reserve_book/<int:book_id>")
@login_required
def reserve_book(book_id, status_list=None):
    reserve = Reserve_operations(session, app)
    user_id = current_user.id
    is_reserve = reserve.book_reservation(book_id, user_id)
    flash(is_reserve)
    return redirect((url_for('home')))


@app.route('/dereserve_book/<int:book_id>/<int:user_id>')
@login_required
def dereserve_book(book_id, user_id):
    dereserve = Dereserve_returns(session, app)
    current_user_id = current_user.id
    is_dereserve = dereserve.book_withdraw(book_id, user_id, current_user_id)
    flash(is_dereserve)
    return redirect((url_for('home')))


@app.route('/book_approvals', methods=['GET', 'POST'])
@login_required
@admin_only
def book_approvals():
    book_approve = Approve_books(session, app)
    current_user_id = current_user.id
    users_with_books, total_reserve_books = book_approve.approval_of_book(current_user_id)
    # flash (users_with_books)
    return render_template('book_approval.html', users_with_books=users_with_books,
                           reserve_books_count=total_reserve_books, logged_in=current_user.is_authenticated)


@app.route('/approved_book/<int:book_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def approved_book(book_id, user_id):
    book_approve = Approve_books(session, app)
    is_approve = book_approve.approved_by_admin(book_id, user_id)
    if is_approve:
        return redirect(url_for('book_approvals'))
    else:
        flash(f'No books are reserved for approval')


@app.route('/return_book/<int:book_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def return_book(book_id, user_id):
    book_return = Dereserve_returns(session, app)
    book_return.book_to_return(book_id, user_id)

    return redirect(url_for('home'))


@app.route('/return_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def renew_book(book_id):
    renewal_books = Reserve_operations(session, app)
    is_renew = renewal_books.renewal_of_book(book_id, user_id=current_user.id)
    flash(is_renew)

    return redirect(url_for('home'))


@app.route("/book_review/<int:book_id>", methods=['GET', 'POST'])
@login_required
def add_book_review(book_id):
    review_form = ReviewForm()
    try:
        book = session.query(Book.id, Book.image).filter(Book.id == book_id).first()
        if book is None:
            # Handle the case where the book with the given ID doesn't exist
            return "Book not found", 404
        if review_form.validate_on_submit():
            if not current_user.is_authenticated:
                flash("You need to login or register to comment.")
                return redirect(url_for("login"))
            soup = BeautifulSoup(review_form.review_text.data, 'html.parser')
            sanitized_content = soup.get_text()
            new_review = Book_Review(
                review_text= sanitized_content,
                book_id=book_id,
                user_id=current_user.id,
            )
            session.add(new_review)
            session.commit()
        book_reviews = session.query(Book_Review.review_text).filter(Book_Review.book_id == book_id).all()

    except Exception as e:
        session.rollback()

    return render_template("book_reviews.html", book=book, form=review_form, reviews=book_reviews,
                           current_user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route('/books_on_loan')
@login_required
def books_on_loan():
    book_loans = Loan_Details(session, app)
    loans = book_loans.loan_books(current_user.id)
    if loans == True:
        return send_from_directory(directory='static', path='reports/loan_database.pdf')
    else:
        flash("No books available")
        return redirect(url_for('home'))


@app.route('/create_file/<file_type>')
@admin_only
@login_required
def create_file(file_type):
    # pass
    reports = Reports(session, app)
    is_created = reports.generate_reports(file_type)
    if is_created == 'excel':
        return render_template('reports.html', msg=is_created, logged_in=current_user.is_authenticated,
                               filetype='excel')
    elif is_created == 'pdf':
        return render_template('reports.html', msg=is_created, logged_in=current_user.is_authenticated,
                               filetype='pdf')
    else:
        return is_created


@app.route('/download/<file_type>')
@admin_only
@login_required
def download(file_type):
    if file_type == 'excel':
        return send_from_directory(directory='static', path='reports/book_database.xlsx')
    elif file_type == 'pdf':
        return send_from_directory(directory='static', path='reports/book_database.pdf')
    else:
        return "No files available"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
