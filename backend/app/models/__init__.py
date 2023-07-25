import re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import and_
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
migrate = Migrate()


class Base(db.Model):
    """ Model that contains base database models. """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save_to_db(self):
        """ Saving into db """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        """  Updating into db """
        for key, value in kwargs.items():
            setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_from_db(self):
        """ Deleting from database """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        """ Find by id """
        return cls.query.filter_by(id=id).first()


class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_disabled = db.Column(db.Boolean, default=False)
    task = db.relationship("Task", cascade="delete")

    @validates("username")
    def username_required(self, key, value):
        if value == "" or value is None:
            raise ValueError(
                "El nombre del usuario es un campo requerido.")
        return value

    @validates("email")
    def email_not_valid(self, key, value):
        email_already_taken = User.query.filter(
            and_(User.id != self.id, User.email == value)
        ).count()
        if email_already_taken > 0:
            raise ValueError(
                "El correo electrónico se encuentra tomado por otro usuario.")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, value):
            return value.lower()
        raise ValueError(
            "El correo electrónico no es válido.")

    def __repr__(self):
        """ String representation  """
        if self.id is not None:
            return "<User '#{}: {}'>".format(
                self.id, self.username)
        return "<User 'NotSaved: {}'>".format(
                    self.username)

    def set_password(self, password):
        """ Setting password for user """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ Checking password for user """
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        """ Find user by email address """
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def exists(email):
        """ Check if user exists """
        user = User.find_by_email(email)
        if user:
            return True
        return False


class Task(Base):
    __tablename__ = 'task'
    task = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @validates("task")
    def task_required(self, key, value):
        if value == "" or value is None:
            raise ValueError(
                "El título de la tarea es un campo requerido.")
        return value

    @validates("description")
    def description_required(self, key, value):
        if value == "" or value is None:
            raise ValueError(
                "La descripción de la tarea es un campo requerido.")
        return value

    def __repr__(self):
        """ String representation  """
        if self.id is not None:
            return "<Task '#{}: {}'>".format(
                self.id, self.task)
        return "<Task 'NotSaved: {}'>".format(
                    self.task)

    def set_as_completed(self, completed=True):
        """ Set task as completed """
        self.is_completed = completed
        self.save_to_db()

    @staticmethod
    def find_all_by_user_id(user_id):
        """ Find user by email address """
        return Task.query.filter_by(user_id=user_id).all()
