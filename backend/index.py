from flask import render_template
from app import app

def page_not_found(error):
    return render_template("not_found.html")


if __name__ == "__main__":
    app.register_error_handler(404, page_not_found),
    app.run(debug=True)