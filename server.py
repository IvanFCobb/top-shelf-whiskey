from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import whiskeys
from flask_app.controllers import comments
from flask_app.controllers import replies


if __name__ == "__main__":
    app.run(debug=True)
