import logging
from flask import Blueprint, request
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)
from flask_restx import Api, Resource, fields
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
from app.routes.utils import authorizations
from app.schemas import TaskSchema, UserSchema, LoginSchema


main = Blueprint("main", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})
api = Api(
    prefix="/api",
    version="1.0",
    title="MentalidadWeb API",
    description="App gestión tareas",
    doc="/api/documentation/",
    authorizations=authorizations,
    security="apikey"
)

# Defining the schemas
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
user_schema = UserSchema()
login_schema = LoginSchema()

login_fields = api.model('LoginResource', {
    "email": fields.String(
        required=True,
        description="The user's account email"
    ),
    "password": fields.String(
        required=True,
        description="The user's account password"
    ),
})
register_fields = api.model('RegisterResource', {
    "email": fields.String(
        required=True,
        description="The user's account email"
    ),
    "password": fields.String(
        required=True,
        description="The user's account password"
    ),
    "username": fields.String(
        required=True,
        description="The user's account username"
    )
})
user_fields = api.model('UserResource', {
    "username": fields.String(
        required=True,
        description="The user's account username"
    ),
    "is_disabled": fields.Boolean(
        required=True,
        description="User status.",
        default=False
    )
})
task_fields = api.model('TaskCreateResource', {
    "task": fields.String(
        required=True,
        description="Task title"
    ),
    "description": fields.String(
        required=False,
        description="Task description"
    ),
    "is_completed": fields.Boolean(
        required=False,
        description="Task status",
        default=False
    ),
    "user_id": fields.Integer(
        required=True,
        description="Unique user ID owner of the task"
    )
})


@api.route("/register", endpoint="register")
class RegisterResource(Resource):
    """Class for register"""

    @api.expect(register_fields, status=201)
    @api.doc(responses={201: "Usuario guardado."})
    @api.doc(responses={400: "La cuenta ya existe o está deshabilitada."})
    def post(self):
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
                    return ERR_EXISTING_USER, 400
                user = User(**args)
                user.set_password(password)
                user.save_to_db()
                return SUC_NEW_USER, 201
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en create_user: {error_message}")
            return ERR_500, 500


@api.route("/login", endpoint="login")
class LoginResource(Resource):
    """Class for auth resources"""

    @api.expect(login_fields, status=200)
    @api.doc(responses={200: "Success"})
    @api.doc(responses={400: "El usuario o la contraseña son incorrectos"})
    def post(self):
        """Endpoint for user login"""
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
                if user is None or user.check_password(password) is False:
                    return ERR_WRONG_USER_PASS, 400

                access_token = create_access_token(email)
                user.is_disabled = False
                user.save_to_db()

                return {
                    "token": access_token,
                    "user": user_schema.dump(user),
                    "email": user.email,
                    "username": user.username,
                    "user_id": user.id,
                }, 200
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en login_user: {error_message}")
            return ERR_500, 500


@api.doc(security="apikey")
@api.route("/user", endpoint="user")
class UserResource(Resource):
    """Function with methods to user"""

    @api.doc(responses={200: "Success"})
    @api.doc(responses={404: "Usuario no encontrado"})
    @jwt_required()
    def get(self):
        """Function to get user info"""
        try:
            email = get_jwt_identity()
            user = User.find_by_email(email)
            if user:
                return user_schema.dump(user), 200

            return ERR_USER_NOT_FOUND, 404

        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en get_user: {error_message}")
            return ERR_500, 500

    @api.expect(user_fields, status=200)
    @api.doc(responses={200: "Success"})
    @api.doc(responses={404: "Usuario no encontrado"})
    @jwt_required()
    def put(self):
        """Function to update user info"""
        try:
            email = get_jwt_identity()
            user = User.find_by_email(email)
            if user is None:
                return ERR_USER_NOT_FOUND, 404
            args_json = request.get_json()
            try:
                user.update(**args_json)
                return SUC_USER_UPDATED, 200
            except Exception as e:
                print(e)
                raise e
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en update_user: {error_message}")
            return ERR_PROCESSING_REQ, 500

    @api.doc(responses={204: "Cuenta deshabilitada."})
    @jwt_required()
    def delete(self):
        """Function to delete user"""
        try:
            email = get_jwt_identity()
            user = User.find_by_email(email)
            user.is_disabled = True
            user.save_to_db()
            return ERR_DISABLED_ACC, 204
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en update_user: {error_message}")
            return ERR_PROCESSING_REQ, 500


@api.doc(security="apikey")
@api.route("/task", endpoint="task")
class TaskCreateResource(Resource):
    """Function with methods to create task"""

    @api.expect(task_fields, status=201)
    @api.doc(responses={201: "Tarea guardada exitósamente"})
    @api.doc(responses={400: "El valor de Tarea no puede estar vacío"})
    @jwt_required()
    def post(self):
        """ Function to post a new task """
        try:
            args_json = request.get_json()
            try:
                args = task_schema.load(args_json)
            except Exception as e:
                print("exep: ", e)
                raise e
            else:
                if not args["task"]:
                    return ERR_TASK_EMPTY, 400
                Task(**args).save_to_db()
                return SUC_TASK_OK, 201
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en create_task: {error_message}")
            return ERR_500, 500


@api.doc(security="apikey")
@api.route("/task/<int:id>", endpoint="task/<int:id>")
class TaskResource(Resource):
    """Function with methods for Task"""

    @api.expect(task_fields, status=200)
    @api.doc(responses={404: "Tarea no encontrada"})
    @api.doc(responses={200: "Tarea modificada con éxito."})
    @jwt_required()
    def put(self, id):
        """ Function to update a task by id """
        try:
            email = get_jwt_identity()
            user = User.find_by_email(email)
            task = Task.find_by_id(id)
            if task is None:
                return ERR_TASK_NOT_FOUND, 404
            if user.id != task.user_id:
                return ERR_TASK_NOT_FOUND, 404
            args_json = request.get_json()
            try:
                task.update(**args_json)
                return SUC_TASK_UPDATED, 200
            except Exception as e:
                print(e)
                raise e
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en update: {error_message}")
            return ERR_500, 500

    @api.doc(responses={204: "Tarea eliminada."})
    @api.doc(responses={404: "Tarea no encontrada"})
    @jwt_required()
    def delete(self, id):
        """ Function to delete a task by id """
        try:
            email = get_jwt_identity()
            user = User.find_by_email(email)
            task = Task.find_by_id(id)
            if task is None:
                return ERR_TASK_NOT_FOUND, 404
            if user.id != task.user_id:
                return ERR_TASK_NOT_FOUND, 404
            task.delete_from_db()
            return SUC_TASK_DELETED, 204
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en update_or_delete_task: {error_message}")
            return ERR_500, 500


@api.doc(security="apikey")
@api.route("/tasklist", endpoint="tasklist")
class TasksResources(Resource):
    """Function to get tasks list"""

    @api.doc(responses={200: "Success"})
    @api.doc(responses={404: "Usuario no encontrado."})
    @jwt_required()
    def get(self):
        """ Function to get the task list """
        try:
            email = get_jwt_identity()
            user = User.find_by_email(email)
            if user is None:
                return ERR_USER_NOT_FOUND, 404
            try:
                tasks = Task.find_all_by_user_id(user.id)
                if tasks:
                    return tasks_schema.dump(tasks), 200

                return ERR_USER_NOT_FOUND, 404

            except Exception as e:
                error_message = str(e)
                logging.error(f"Error en get_tasks: {error_message}")
                return ERR_500, 500
        except Exception as e:
            error_message = str(e)
            logging.error(f"Error en get_tasks: {error_message}")
            return ERR_500, 500
