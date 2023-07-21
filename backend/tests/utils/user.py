from app.models import User


def save_user_to_db(data):
    """ Save user to db """
    password = data.get("password", None)
    user = User(**data)
    user.set_password(password)
    user.save_to_db()
    return user
