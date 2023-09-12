import datetime as dt
import os
from flask import flash, redirect, request, url_for, render_template, send_from_directory
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename
from library.python_files.Database_tables import Book, Book_Copies, User, Book_Status


class Review():
    def __init__(self, session, app):
        self.session = session
        self.app = app

    def review_book(self,book_id,user_id):
        try:
            book = self.session.query(Book.id, Book.image).filter(Book.id == book_id).first()
            if book is None:
                # Handle the case where the book with the given ID doesn't exist
                return "Book not found", 404
            if review_form.validate_on_submit():
                if not current_user.is_authenticated:
                    flash("You need to login or register to comment.")
                    return redirect(url_for("login"))
                new_review = Book_Review(
                    review_text=review_form.review_text.data,
                    book_id=book_id,
                    user_id=current_user.id,
                    # user_review=current_user,
                    # book_review=book
                )
                session.add(new_review)
                session.commit()
            book_reviews = session.query(Book_Review.review_text).filter(Book_Review.book_id == book_id).all()


        except Exception as e:
            session.rollback()
