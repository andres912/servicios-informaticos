from project import create_app
from flask import app

app = create_app("../instance/flask.cfg")
if __name__ == "__main__":
    app.run()