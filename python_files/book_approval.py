from flask import flash, redirect, request, url_for
from library.python_files.Database_tables import Book, Book_Copies, Book_Status, User
from sqlalchemy import text
from sqlalchemy.orm import aliased
import datetime as dt


def reserve_books_count(user_id, session):
    total_reserve_books = session.query(Book_Status).filter(Book_Status.user_id == user_id,
                                                            Book_Status.book_approvals_status == 'Reserved').count()
    if not total_reserve_books:
        return 0
    else:
        return total_reserve_books


class Approve_books:
    def __init__(self, session, app):
        self.session = session
        self.app = app

    def approval_of_book(self,current_user_id):
        bs = aliased(Book_Status, name='bs')
        users_with_books = self.session.query(User.first_name, User.id.label("user_id"), Book.id, Book.title,
                                              bs.book_approvals_status,
                                              bs.return_book_date, bs.approve_book_date).join(
            Book).join(User).filter(bs.book_id == Book.id).all()

        total_reserve_books = reserve_books_count(current_user_id, self.session)
        if not users_with_books:
            return 'No books are available to Approve!!', total_reserve_books
        else:
            return users_with_books, total_reserve_books

    def approved_by_admin(self, book_id, user_id):
        all_approved_status = self.session.query(Book_Status).filter(Book_Status.book_id == book_id).all()
        for approved_status in all_approved_status:
            if approved_status.book_approvals_status == 'Reserved':
                query = text(
                    "UPDATE books_status "
                    "SET book_approvals_status = 'Approved', approve_book_date='current_date'"
                    "WHERE id = :book_id AND user_id = :user_id AND book_approvals_status = 'Reserved'")
                self.session.execute(query, {"book_id": book_id, "user_id": user_id})
                self.session.commit()
                approved_status.book_approvals_status = "Approved"
                current_date = dt.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
                approved_status.approve_book_date = current_date
                approve_date = dt.datetime.strptime(current_date, "%m-%d-%Y, %H:%M:%S")
                approved_status.return_book_date = str(approve_date + dt.timedelta(days=7))
                self.session.commit()
                return True
