import datetime as dt
from flask import Flask, render_template, redirect, url_for, flash, request,send_from_directory
from flask_bootstrap import Bootstrap
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from werkzeug.utils import secure_filename
from forms import RegisterForm, LoginForm, BookdetailsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
bootstrap = Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_temp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#upload the image
UPLOAD_FOLDER = './static/books' # where to store uploaded files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Book(db.Model):
    __tablename__ = "book_details"
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=False)
    book_author = db.Column(db.String(100), unique=False)
    book_image = db.Column(db.String(100), unique=False)
    date = db.Column(db.Text)


with app.app_context():
    db.create_all()


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    current_date = dt.datetime.today()
    book_data=Book.query.all()
    return render_template("index_temp.html", date=current_date,books=book_data)

@app.route('/')
def login():
    pass
@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    pass

@app.route('/add_book', methods=['GET','POST'])
def add_book_details():
    book_form = BookdetailsForm();
    if book_form.validate_on_submit():
        file = book_form.image.data
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url=url_for('get_file',filename=filename)
            book =Book()
            book.book_name = book_form .bookname.data
            book.book_author = book_form .author.data
            book.book_image = file_url
            book.date= dt.datetime.now()
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add_book_details.html', form=book_form)


    # return redirect(url_for('uploaded_file',filename=filename))

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

if __name__ == "__main__":
    app.run(debug=True)
