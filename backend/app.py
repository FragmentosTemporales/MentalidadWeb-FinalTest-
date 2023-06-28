"""Importing necessary Flask modules for creating and handling HTTP requests and responses"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


from models.db import db
from routes.main import main


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["JWT_SECRET_KEY"] = "super-secret"
app.register_blueprint(main)
db.init_app(app)

migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)
