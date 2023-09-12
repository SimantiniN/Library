import datetime as dt
import os
from flask import flash, redirect, request, url_for
from werkzeug.utils import secure_filename
from library.python_files.Database_tables import Book, Book_Copies

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Add_Book_To_DB:
    def __init__(self, session, app):
        self.session = session
        self.app = app

    def add_book_to_db(self, book_form):
        book_exist = False
        books = self.session.query(Book).all()
        for book in books:
            if book.title == book_form.title.data.title():
                # book_exist = True
                if book_exist:
                    return 'Book is already exist'
                    # book_exist = False
                    # return redirect(url_for('home'))

        file = book_form.image.data
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('get_file', filename=filename)
            book = Book()
            book.title = book_form.title.data.title()
            book.sub_title = book_form.subtitle.data
            book.author = book_form.author.data
            book.brand_name = book_form.brand_name.data
            book.number_of_pages = book_form.number_of_pages.data
            book.book_contains = book_form.book_contains.data
            book.isbn = book_form.isbn.data
            book.image = file_url
            book.no_of_copies = book_form.no_of_copies.data
            self.session.add(book)
            self.session.commit()
            total_book_copies = Book_Copies()
            total_book_copies.book_id = book.id
            total_book_copies.remaining_copies = book.no_of_copies
            self.session.add(total_book_copies)
            self.session.commit()
            return 'Book added successfully'

    def update_book(self, edit_form, book_id, book_to_edit):
        book_to_edit.title = edit_form.title.data
        book_to_edit.sub_title = edit_form.sub_title.data
        book_to_edit.author = edit_form.author.data
        book_to_edit.brand_name = edit_form.brand_name.data
        book_to_edit.number_of_pages = edit_form.number_of_pages.data
        book_to_edit.book_contains = edit_form.book_contains.data
        book_to_edit.isbn = edit_form.isbn.data
        book_to_edit.no_of_copies = edit_form.no_of_copies.data
        file = edit_form.image.data
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('get_file', filename=filename)
            book_to_edit.image = file_url
            # book_to_edit.date = dt.datetime.now()
            # session.add(book_to_edit)
            self.session.commit()
        return True

    def deletion_of_book(self, book_id):
        book_to_delete = self.session.query(Book).filter(Book.id == book_id).first()
        self.session.delete(book_to_delete)
        self.session.commit()
        return 'Book deleted successfully'
