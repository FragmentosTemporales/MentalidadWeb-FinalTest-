import logging
from flask import Blueprint, jsonify, render_template, request
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from app.messages import (
    ERR_500,
    ERR_DISABLED_ACC,
    ERR_EXISTING_USER,
    ERR_PROCESSING_REQ,
    ERR_USER_NOT_FOUND,
    ERR_TASK_EMPTY,
    ERR_TASK_NOT_FOUND,
    ERR_WRONG_USER_PASS,
    SUC_NEW_USER,
    SUC_TASK_OK,
    SUC_TASK_UPDATED,
    SUC_TASK_DELETED,
    SUC_USER_UPDATED,
)
from app.models import User, Task
from app.schemas import TaskSchema, UserSchema, LoginSchema


main = Blueprint("main", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})

# Defining the schemas
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
user_schema = UserSchema()
login_schema = LoginSchema()


@main.route("/")
def home():
    """ Home function """
    return render_template("index.html")


@main.route("/register", methods=["POST"])
def create_user():
    """Function to create user"""
    try:
        args_json = request.get_json()
        try:
            args = user_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            user_exists = User.exists(email)
            if user_exists:
                return jsonify(ERR_EXISTING_USER), 400
            user = User(**args)
            user.set_password(password)
            user.save_to_db()
            return jsonify(SUC_NEW_USER), 201
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/login", methods=["POST"])
def login_user():
    """ Function to log in """
    try:
        args_json = request.get_json()
        try:
            args = login_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            user = User.find_by_email(email)
            if user is None or \
               user.check_password(password) is False:
                return jsonify(ERR_WRONG_USER_PASS), 400

            access_token = create_access_token(email)
            user.is_disabled = False
            user.save_to_db()

            return jsonify(
                    {
                        "token": access_token,
                        "user": user_schema.dump(user),
                        "email": user.email,
                        "username": user.username,
                        "user_id": user.id,
                    }
            ), 200
    except Exception as e:
        error_message = str(e)
        print(e)
        logging.error(f"Error en login_user: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/user/<int:user_id>")
def get_user(user_id):
    """ Return user info by id """
    try:
        user = User.find_by_id(user_id)
        if user:
            print(user)
            return jsonify(user_schema.dump(user))

        return jsonify(ERR_USER_NOT_FOUND), 404

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_user: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/userlist/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(id):
    """ Function to update username """
    try:
        user = User.find_by_id(id)
        if user is None:
            return jsonify(ERR_USER_NOT_FOUND), 404
        if request.method == "DELETE":
            user.is_disabled = True
            user.save_to_db()
            return jsonify(ERR_DISABLED_ACC), 204
        user.username = request.json.get("username")
        user.save_to_db()
        return jsonify(SUC_USER_UPDATED), 200
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en update_user: {error_message}")
        return jsonify(ERR_PROCESSING_REQ), 500


@main.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    """ Function to create a task """
    try:
        args_json = request.get_json()

        try:
            args = task_schema.load(args_json)
        except Exception as e:
            print("exep: ", e)
            raise e
        else:
            if not args["task"]:
                return jsonify(ERR_TASK_EMPTY), 400
            Task(**args).save_to_db()
            return jsonify(SUC_TASK_OK), 201
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_task: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/tasklist/<int:user_id>", methods=["GET"])
@jwt_required()
def get_tasks(user_id):
    """ Function to get tasklist by user id """
    try:
        email = get_jwt_identity()
        user = User.find_by_email(email)
        if user == None:
            return jsonify(ERR_USER_NOT_FOUND), 404
        try:
            tasks = Task.find_all_by_user_id(user_id)
            if tasks:
                return jsonify(tasks_schema.dump(tasks)), 200

            return jsonify(ERR_USER_NOT_FOUND), 404

        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en get_tasks: {error_message}")
            return jsonify(ERR_500), 500           
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_tasks: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/task/<int:id>", methods=["DELETE", "PUT"])
@jwt_required()
def update_or_delete_task(id):
    """ Function to delete or update task by id """
    try:
        email = get_jwt_identity()
        user = User.find_by_email(email)
        task = Task.find_by_id(id)
        if task is None:
            return jsonify(ERR_TASK_NOT_FOUND), 404
        if user.id != task.user_id:
            return jsonify(ERR_TASK_NOT_FOUND), 404
        if request.method == "DELETE":
            task.delete_from_db()
            return jsonify(SUC_TASK_DELETED), 204
        args_json = request.get_json()
        try:
            task.update(**args_json)
            return jsonify(SUC_TASK_UPDATED), 200
        except Exception as e:
            print(e)
            raise e
            
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en update_or_delete_task: {error_message}")
        return jsonify(ERR_500), 500
