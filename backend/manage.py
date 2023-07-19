import click
from werkzeug.security import generate_password_hash
from flask.cli import FlaskGroup
from app import create_app
from app.models import db, User


cli = FlaskGroup(create_app=create_app)


@cli.command("greeting")
@click.option("--name", required=True)
@click.option("--age", type=int, required=True)
def greeting(name, age):
    """ Make greeting from command line interface """
    greeting = f"Hi {name}! You are {age} years old. Have a nice day!"
    print(greeting)


@cli.command("create-user")
@click.option("--username", required=True)
@click.option("--email", required=True)
@click.option("--password", required=True)
def create_user(username, email, password):
    """ Create user in the platform by command line interface """
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return "ERROR: El usuario ya existe en la plataforma"
    password_hash = generate_password_hash(password)
    try:
        user = User(username=username, password=password_hash, email=email)
        user.save_to_db()
    except Exception as e:
        print(e)
        raise e


if __name__ == "__main__":
    cli()
