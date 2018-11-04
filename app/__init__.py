from flask import Flask
from app.config import Config
app = Flask(__name__)
app.config.from_object(Config)

from app import routes

if __name__ == "__main__":
    app.run(host='0.0.0.0')

