from app import app
from app.controllers import users
from app.controllers import whiskeys
from app.controllers import comments
from app.controllers import replies


if __name__ == "__main__":
    app.run(debug=True)
