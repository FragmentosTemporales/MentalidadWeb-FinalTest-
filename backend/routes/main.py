import logging
from flask import  request, jsonify, render_template, Blueprint
from flask_bcrypt import  generate_password_hash, check_password_hash
from flask_jwt_extended import  jwt_required, create_access_token


from models.db import db, User, Task

main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Esta función retorna la vista Home del proyecto, esta vista está creada con HTML"""
    return render_template("index.html")


@main.route("/register", methods=["POST"])
def create_user():
    """Recibe parámetros a través de la consulta y crea el usuario."""
    try:
        username = request.json.get("username")
        email = request.json.get("email")
        password = request.json.get("password")
        password_hash = generate_password_hash(password)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            if existing_user.isDisabled:
                return (
                    jsonify(
                        {
                            "error": "La cuenta está deshabilitada, inicia sesión para habilitar."
                        }
                    ),
                    400,
                )

            return jsonify({"error": "El correo ya existe en la base de datos."}), 400

        new_user = User(username=username, email=email, password=password_hash)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario guardado"}), 201
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500


@main.route("/login", methods=["POST"])
def login_user():
    """Recibe parámetros a través de la consulta y retorna un token"""
    try:
        email = request.json.get("email")
        password = request.json.get("password")
        user = User.query.filter_by(email=email).first()

        if user is not None:
            is_valid = check_password_hash(user.password, password)

            if is_valid:
                access_token = create_access_token(identity=email)
                user.isDisabled = False
                db.session.commit()

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

            return jsonify({"error": "La contraseña es incorrecta"}), 400

        return (
            jsonify({"error": "El usuario no existe o la información es inválida"}),
            400,
        )

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en login_user: {error_message}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500


@main.route("/user/<int:user_id>")
def get_user(user_id):
    """Retorna la información del usuario según su ID"""
    try:
        user = User.query.filter_by(id=user_id).first()

        if user is not None:
            return jsonify(user.serialize())

        return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_user: {error_message}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500


@main.route("/userlist/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(id):
    """Recibe parámetros para actualizar o deshabilitar al usuario"""
    try:
        user = User.query.get(id)

        if user is not None:
            if request.method == "DELETE":
                user.isDisabled = True
                db.session.commit()
                return jsonify({"message": "Cuenta deshabilitada."}), 204

            user.username = request.json.get("username")

            db.session.commit()
            return jsonify({"message": "Usuario actualizado"}), 200

        return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en update_user: {error_message}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500


@main.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    """Recibe parámetros para crear la tarea."""
    try:
        task = request.json.get("task")
        description = request.json.get("description")
        user_id = request.json.get("user_id")

        if not task:
            return jsonify({"error": "El valor de Tarea no puede estar vacío"}), 400

        new_task = Task(task=task, description=description, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "Tarea guardada exitósamente"}), 201

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_task: {error_message}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500


@main.route("/tasklist/<int:user_id>", methods=["GET"])
@jwt_required()
def get_tasks(user_id):
    """Retorna lista de tareas del usuario encontrado por el ID"""
    try:
        tasks = Task.query.filter_by(user_id=user_id).all()
        tasks_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "task": task.task,
                "description": task.description,
                "user_id": task.user_id,
                "isCompleted": task.isCompleted,
            }
            tasks_list.append(task_dict)
        return jsonify(tasks_list), 200

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_tasks: {error_message}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500


@main.route("/task/<int:id>", methods=["DELETE", "PUT"])
@jwt_required()
def update_or_delete_task(id):
    """Recibe parámetros de la tarea a modificar o eliminar"""
    try:
        task = Task.query.get(id)
        if task is None:
            return jsonify({"error": "Tarea no encontrada"}), 404

        if request.method == "DELETE":
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Tarea eliminada"}), 204

        task.task = request.json.get("task", task.task)
        task.description = request.json.get("description", task.description)

        is_completed = request.json.get("isCompleted")
        if is_completed is not None:
            task.isCompleted = bool(is_completed)

        db.session.commit()
        return jsonify({"message": "Tarea modificada con éxito."}), 200

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en update_or_delete_task: {error_message}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500
