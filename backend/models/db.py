from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    isDisabled = db.Column(db.Boolean, default=False)
    task = db.relationship("Task", cascade="delete")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "isDisabled": self.isDisabled
        }


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    isCompleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def serialize(self):
        return {
            "id": self.id,
            "task": self.task,
            "description": self.description,
            "user_id" :  self.user_id
        }