from flask import flash, redirect, request, url_for
from library.python_files.Database_tables import Book, Book_Copies, Book_Status
from sqlalchemy import text
import datetime as dt


class Reserve_operations:
    def __init__(self, session, app):
        self.session = session
        self.app = app

    def book_reservation(self, book_id, user_id):
        book = self.session.query(Book.title, Book.id, Book.no_of_copies, Book_Copies.remaining_copies).join(
            Book_Copies,
            Book_Copies.book_id == book_id).filter(
            Book.id == book_id).first()
        if not book:
            flash('Book not found!', 'error')
            return redirect((url_for('home')))
        elif book.no_of_copies > 0:
            with self.session.no_autoflush:
                status_list = self.session.query(Book_Status.book_approvals_status, Book_Status.user_id).filter(
                    Book_Status.book_id == book_id, Book_Status.user_id == user_id).all()
            if not status_list and book.remaining_copies > 0:
                different_user_book_status = Book_Status(book_id=book_id, user_id=user_id,
                                                         reserve_book_date=dt.datetime.now().strftime(
                                                             "%m-%d-%Y, %H:%M:%S"),
                                                         book_approvals_status="Reserved")
                self.session.add(different_user_book_status)
                self.session.query(Book_Copies).filter_by(book_id=book_id)\
                    .update({'remaining_copies': book.remaining_copies - 1})

                self.session.commit()
                return f'Book "{book.title}" reserved successfully!', 'success'

            elif book.remaining_copies > 0:
                for status in status_list:
                    if status.book_approvals_status == 'Reserved' and status.user_id == user_id:
                        return 'Book is already reserved!🤷'  # +'error'
                    elif status.book_approvals_status == 'Approved' and status.user_id == user_id:
                        return 'Book is already Approved!🤷‍'
                    elif status.book_approvals_status == 'Waiting' and status.user_id == user_id:
                        return 'Book is already in Waiting List !🤷‍'
                    else:
                        different_user_book_status = Book_Status(book_id=book_id, user_id=user_id,
                                                                 reserve_book_date=dt.datetime.now().strftime(
                                                                     "%m-%d-%Y, %H:%M:%S"),
                                                                 book_approvals_status="Reserved")
                        self.session.add(different_user_book_status)
                        query = text(
                            "UPDATE Book_Copies "
                            "SET remaining_copies  = :current_remaining_copies WHERE book_id = :book_id")
                        self.session.execute(query,
                                             {"book_id": book_id,
                                              "current_remaining_copies": book.remaining_copies - 1})
                        self.session.commit()
                        return f'Book "{book.title}" reserved successfully!' + 'success'

            else:
                status_list = self.session.query(Book_Status.book_approvals_status, Book_Status.user_id).filter(
                Book_Status.book_id == book_id).all()
                for status in status_list:
                    if status.user_id == user_id:
                        if status.book_approvals_status == 'Reserved':
                            return 'Book is already reserved!🤷'
                        elif status.book_approvals_status == 'Approved':
                            return 'Book is already Approved!🤷‍', 'error'
                        elif status.book_approvals_status == 'Waiting':
                            return 'Book is already in Waiting List !🤷‍'
                        else:
                            different_user_book_status = Book_Status(book_id=book_id, user_id=user_id,
                                                                     reserve_book_date=dt.datetime.now().strftime(
                                                                         "%m-%d-%Y, %H:%M:%S"),
                                                                     book_approvals_status="Waiting")
                            self.session.add(different_user_book_status)
                            self.session.commit()
                            return 'Currently not available !!You are in In waiting list'
                    else:
                        different_user_book_status = Book_Status(book_id=book_id, user_id=user_id,
                                                                 reserve_book_date=dt.datetime.now().strftime(
                                                                     "%m-%d-%Y, %H:%M:%S"),
                                                                 book_approvals_status="Waiting")

                        self.session.add(different_user_book_status)
                        self.session.commit()
                        return 'Currently not available !!You are in In waiting list'
        else:
            return "no copies available"

    def renewal_of_book(self, book_id, user_id):
        with self.session.no_autoflush:
            book_status = self.session.query(Book_Status).filter(Book_Status.book_id == book_id).all()
        if book_status:
            for status in book_status:
                if status.book_approvals_status == "Waiting" and status.user_id == user_id:
                    return "Cannot renew book as others are in waiting list."
                elif status.book_approvals_status == "Approved" and status.user_id == user_id:
                    current_date = dt.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
                    status.approve_book_date = current_date
                    approve_date = dt.datetime.strptime(current_date, "%m-%d-%Y, %H:%M:%S")
                    status.return_book_date = str(approve_date + dt.timedelta(days=7))
                    self.session.commit()
                    return f"Renewed book successfully.Return you book on{status.return_book_date}"
                else:
                    return "No book found for renewal"
        else:
            return "No book found for renewal"
