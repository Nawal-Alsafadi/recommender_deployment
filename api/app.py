from flask import Flask
from flask_cors import CORS
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.routes.app_routes import app_routes
from api.utils.first_init import FirstInit




app = Flask(__name__)
app.debug = True
CORS(app)
app_routes(app)


@app.route('/')
def index():
    return "Hola!"

@app.route('/second_page')
def index2():
    return "Hola from second page !!"

if __name__ == "__main__":
    app.run()



