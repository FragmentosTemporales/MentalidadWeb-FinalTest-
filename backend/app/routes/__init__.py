import logging
from flask import request, jsonify, render_template, Blueprint
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User, Task


main = Blueprint("main", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})
SUC_USER_UPDATED = {
    "message": "Usuario actualizado"
}
ERR_EXISTING_USER = {
    "error": "La cuenta ya existe o está deshabilitada."
}
ERR_EXISTING_EMAIL = {
    "error": "El correo ya existe en la base de datos."
}
ERR_WRONG_USER_PASS = {
    "error": "El usuario o la contraseña son incorrectos"
}
ERR_PROCESSING_REQ = {
    "error": "Error al procesar la solicitud"
}
ERR_DISABLED_ACC = {
    "error": "Cuenta deshabilitada."
}
ERR_USER_NOT_FOUND = {
    "error": "Usuario no encontrado"
}
ERR_TASK_EMPTY = {
    "error": "El valor de Tarea no puede estar vacío"
}
SUC_TASK_OK = {
    "message": "Tarea guardada exitósamente"
}
ERR_500 = {
    "error": "Error al procesar la solicitud"
}
SUC_NEW_USER = {
    "message": "Usuario guardado"
}
ERR_TASK_NOT_FOUND = {
    "error": "Tarea no encontrada"
}
SUC_TASK_UPDATED = {
    "message": "Tarea modificada con éxito."
}
SUC_TASK_DELETED = {
    "message": "Tarea eliminada"
}
ERR_USER_NOT_FOUND = {
    "error": "Usuario no encontrado"
}


@main.route("/")
def home():
    """
        Esta función retorna la vista Home del proyecto, esta vista está
        creada con HTML
    """
    return render_template("index.html")


@main.route("/register", methods=["POST"])
def create_user():
    """Recibe parámetros a través de la consulta y crea el usuario."""
    try:
        username = request.json.get("username")
        email = request.json.get("email")
        password = request.json.get("password")
        password_hash = generate_password_hash(password)
        existing_user = User.find_by_email(email)
        if existing_user or \
           (isinstance(existing_user, User) and existing_user.is_disabled):
            return jsonify(ERR_EXISTING_USER), 400
        data = {
            "username": username,
            "email": email,
            "password": password_hash
        }
        user = User(**data)
        user.save_to_db()
        return jsonify(SUC_NEW_USER), 201
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")
        raise e
        return jsonify(ERR_500), 500


@main.route("/login", methods=["POST"])
def login_user():
    """Recibe parámetros a través de la consulta y retorna un token"""
    try:
        email = request.json.get("email")
        password = request.json.get("password")
        user = User.find_by_email(email)

        if user is None:
            return jsonify(ERR_WRONG_USER_PASS), 400

        is_valid = check_password_hash(user.password, password)
        if not is_valid:
            return jsonify(ERR_WRONG_USER_PASS), 400
        
        access_token = create_access_token(email)
        user.is_disabled = False
        user.save_to_db()

        return (
            jsonify(
                {
                    "token": access_token,
                    "user_id": user.id,
                    "email": user.email,
                    "username": user.username,
                }
            ),
            200,
        )
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en login_user: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/user/<int:user_id>")
def get_user(user_id):
    """Retorna la información del usuario según su ID"""
    try:
        user = User.find_by_id(user_id)
        if user is not None:
            return jsonify(user.serialize())

        return jsonify(ERR_USER_NOT_FOUND), 404

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_user: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/userlist/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(id):
    """Recibe parámetros para actualizar o deshabilitar al usuario"""
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
    """Recibe parámetros para crear la tarea."""
    try:
        title = request.json.get("task")
        description = request.json.get("description")
        user_id = request.json.get("user_id")
        if not title:
            return jsonify(ERR_TASK_EMPTY), 400
        task = Task(task=title, description=description, user_id=user_id)
        task.save_to_db()
        return jsonify(SUC_TASK_OK), 201
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_task: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/tasklist/<int:user_id>", methods=["GET"])
@jwt_required()
def get_tasks(user_id):
    """Retorna lista de tareas del usuario encontrado por el ID"""
    try:
        tasks = Task.find_all_by_user_id(user_id)
        tasks_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "task": task.task,
                "description": task.description,
                "user_id": task.user_id,
                "is_completed": task.is_completed,
            }
            tasks_list.append(task_dict)
        return jsonify(tasks_list), 200

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_tasks: {error_message}")
        return jsonify(ERR_500), 500


@main.route("/task/<int:id>", methods=["DELETE", "PUT"])
@jwt_required()
def update_or_delete_task(id):
    """Recibe parámetros de la tarea a modificar o eliminar"""
    try:
        task = Task.find_by_id(id)
        if task is None:
            return jsonify(ERR_TASK_NOT_FOUND), 404

        if request.method == "DELETE":
            task.delete_from_db()
            return jsonify(SUC_TASK_DELETED), 204

        print(request.json)
        task.task = request.json.get("task", task.task)
        task.description = request.json.get("description", task.description)
        task.is_completed = request.json.get("is_completed")
        task.save_to_db()
        return jsonify(SUC_TASK_UPDATED), 200

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en update_or_delete_task: {error_message}")
        return jsonify(ERR_500), 500
