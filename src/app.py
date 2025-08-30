from Flask import Flask
from .extensions import db_init
from .routes import register_blueprints
from .commands import register_commands

from dotenv import dotenv_values
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
os.makedirs(IMAGE_FOLDER, exist_ok=True)

DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'pinmonkey.db')

PM_CONF = dotenv_values('pinmonkey.env')

SECRET_KEY = PM_CONF['PM_FLASK_SECRET']

if not SECRET_KEY:
    print("ERROR: No secret key")
    sys.exit(1)

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

Session, engine = db_init(DATABASE_URL)

register_blueprints(app)
register_commands(app)

def get_session():
    return Session

def get_engine():
    return engine
