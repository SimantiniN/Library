from sqlalchemy.orm import relationship, Session, aliased, DeclarativeBase, sessionmaker
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Session, aliased, DeclarativeBase, sessionmaker
import sqlalchemy as db
from sqlalchemy import create_engine, ForeignKey, text, Integer, String, ForeignKeyConstraint

engine = create_engine('sqlite:///Librarysqlachmy.db')

# CONFIGURE TABLES
class Base(DeclarativeBase):
    pass
# Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    all_users_status = relationship("Book_Status", back_populates="user_status")
    users_review = relationship("Book_Review", back_populates="user_review")
    all_users_role = relationship("User_Role", back_populates="user_role")


class User_Role(Base):
    __tablename__ = 'users_role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    description = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user_role = relationship("User", back_populates="all_users_role")


class Book(Base):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    sub_title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    brand_name = db.Column(db.String(100))
    number_of_pages = db.Column(db.Integer)
    book_contains = db.Column(db.String(100))
    isbn = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(100), unique=False)
    no_of_copies = db.Column(db.Integer)
    all_book_status = relationship("Book_Status", back_populates="book_status_all")
    book_reviews = relationship("Book_Review", back_populates='book_review')
    book_copy = relationship("Book_Copies", back_populates="book_copies")


class Book_Copies(Base):
    __tablename__ = 'book_copies'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    book_copies = relationship("Book", back_populates="book_copy")
    remaining_copies = db.Column(db.Integer, unique=False)
    # book_avialabity


class Book_Status(Base):
    __tablename__ = 'books_status'
    id = db.Column(db.Integer, primary_key=True)
    book_approvals_status = db.Column(db.String(50))
    reserve_book_date = db.Column(db.String)
    approve_book_date = db.Column(db.String)
    return_book_date = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    book_status_all = relationship("Book", back_populates="all_book_status")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user_status = relationship("User", back_populates="all_users_status")


class Book_Review(Base):
    __tablename__ = "book_review"
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    book_review = relationship("Book", back_populates="book_reviews")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user_review = relationship("User", back_populates="users_review")


Base.metadata.create_all(engine)
# with app.app_context():
#     db.create_all()
