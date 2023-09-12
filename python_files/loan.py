import datetime as dt
import os
from flask import flash, redirect, request, url_for, render_template, send_from_directory
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename
from library.python_files.Database_tables import Book, Book_Copies, User, Book_Status
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def loan_details_pdf(book_list):
    doc = SimpleDocTemplate("./static/reports/loan_database.pdf", pagesize=letter)

    # Create a list to hold the table data
    table_data = []

    # Define table column headers
    table_data.append(["Book Title", "Book Approvals Status", "Approve Date", "Return Date"])

    # Populate the table with data from all_data
    for data in book_list:
        row = [
            data.title,
            data.book_approvals_status,
            data.approve_book_date,
            data.return_book_date

        ]
        table_data.append(row)

    # Create the table and define table style
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Build the PDF document
    doc.build([table])
    # return "PDF file created successfully!"
    # return True


class Loan_Details:
    def __init__(self, session, app):
        self.session = session
        self.app = app

    def loan_books(self, user_id):
        book_list = []
        books_on_loan = self.session.query(Book.title, Book_Status.book_approvals_status, Book_Status.approve_book_date,
                                           Book_Status.return_book_date) \
            .join(Book_Status) \
            .filter(Book_Status.user_id == user_id).all()
        if books_on_loan:
            for book in books_on_loan:
                book_list.append(book)
                loan_details_pdf(book_list)
            return True
        else:
            return False  # "No books available"
