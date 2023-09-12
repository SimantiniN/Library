from flask import flash, redirect, request, url_for
from library.python_files.Database_tables import Book, Book_Copies, Book_Status
from sqlalchemy import text
import datetime as dt

book_list = []


def dereserve_return(book_id, session):
    return_date_by_another_user = dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    book_status = session.query(Book_Status.book_approvals_status, Book_Status.user_id, Book_Copies.remaining_copies) \
        .join(Book_Copies, Book_Copies.book_id == Book_Status.book_id) \
        .filter(Book_Status.book_approvals_status == 'Waiting', Book_Status.book_id == book_id) \
        .order_by(Book_Status.reserve_book_date) \
        .first()

    if book_status:
        session.query(Book_Status).filter_by(user_id=book_status.user_id, book_approvals_status="Waiting").update(
            {'book_approvals_status': 'Reserved', 'reserve_book_date': return_date_by_another_user}
        )
        query = text("UPDATE book_copies SET remaining_copies = :rem_copies WHERE book_id = :book_id ")
        session.execute(query, {"book_id": book_id, "rem_copies": book_status.remaining_copies - 1})
        session.commit()

class Dereserve_returns:
    def __init__(self, session, app):
        self.session = session
        self.app = app

    def book_withdraw(self, book_id, user_id, current_user_id):
        book = self.session.query(Book.title, Book_Status.book_approvals_status, Book_Status.user_id,
                                  Book_Status.book_id,
                                  Book_Copies.remaining_copies). \
            join(Book_Status).join(Book_Copies). \
            filter(Book_Status.book_id == book_id, Book_Status.user_id == user_id).first()
        if book is None:
            return 'Book not found!'

        elif book.book_approvals_status == "Approved":
            return 'Your book is already approved cannot dereserve'
        elif book.book_approvals_status == 'Waiting':
            book_to_dereserve = self.session.query(Book_Status).filter(Book_Status.book_id == book_id,
                                                                       Book_Status.user_id == user_id).delete()
            self.session.commit()
            return f'Book "{book.title}" deserved successfully!'
        else:
            if book.book_approvals_status == 'Reserved' and book.user_id == current_user_id:
                return_date_by_another_user = dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                book_to_dereserve = self.session.query(Book_Status).filter(Book_Status.book_id == book_id,
                                                                           Book_Status.user_id == user_id).delete()
                query = text("UPDATE book_copies SET remaining_copies = :rem_copies WHERE book_id = :book_id ")
                self.session.execute(query, {"book_id": book_id, "rem_copies": book.remaining_copies + 1})
                self.session.commit()
                dereserve_return(book_id, self.session)
                return f'Book "{book.title}" dereserved successfully!'

    def book_to_return(self, book_id, user_id):
        book = self.session.query(Book.title, Book_Status.book_approvals_status, Book_Status.user_id,
                                  Book_Status.book_id,
                                  Book_Copies.remaining_copies). \
            join(Book_Status).join(Book_Copies). \
            filter(Book_Status.book_id == book_id, Book_Status.user_id == user_id).first()
        if book is None:
            flash('Book not found!', 'error')
        else:
            if book.book_approvals_status == "Approved" and book.user_id == user_id:
                book_to_return = self.session.query(Book_Status).filter(Book_Status.book_id == book_id,
                                                                        Book_Status.user_id == user_id).delete()
                self.session.query(Book_Copies).filter_by(book_id=book_id).update(
                    {'remaining_copies': book.remaining_copies + 1})
                self.session.commit()
                dereserve_return(book_id, self.session)
