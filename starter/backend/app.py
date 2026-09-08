import sys
import os

# Backend root directory ko path mein add karein
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from movies.movies_api import movies_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(movies_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
