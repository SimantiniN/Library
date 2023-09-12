from flask import flash, redirect, request, url_for
from werkzeug.utils import secure_filename
import os
from library.python_files.Database_tables import User
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user


class Registration:
    def __init__(self, session, app):
        self.session = session
        self.app = app
        self.bcrypt = Bcrypt(app)

    def user_registration(self, registration_form):
        if self.session.query(User).filter_by(email=request.form.get('email')).first():
            return True
        hash_and_salted_password = self.bcrypt.generate_password_hash(request.form.get('password'), 10)
        new_user = User()
        new_user.first_name = registration_form.firstname.data
        new_user.last_name = registration_form.lastname.data
        new_user.email = registration_form.email.data
        new_user.password = hash_and_salted_password
        self.session.add(new_user)
        self.session.commit()

    def user_login(self, login_form):
        email = login_form.email.data
        password = login_form.password.data
        user = self.session.query(User).filter_by(email=email).first()
        if user and self.bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return True
        else:
            return False
