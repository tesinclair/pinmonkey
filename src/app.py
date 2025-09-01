from flask import Flask, redirect, url_for
from .extensions import db_init
from .routes.shop import shop_bp
from .routes.basket import basket_bp 
from .routes.home import home_bp
from .routes.checkout import checkout_bp
from .commands import *

from dotenv import dotenv_values
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
os.makedirs(IMAGE_FOLDER, exist_ok=True)

DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'pinmonkey.db')

PM_CONF = dotenv_values('../pinmonkey.env')

SECRET_KEY = PM_CONF.get('PM_FLASK_SECRET')

if not SECRET_KEY:
    print("ERROR: No secret key")
    sys.exit(1)

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

app.config['DB_SESSION'], app.config['DB_ENGINE'] = db_init(DATABASE_URL)

app.register_blueprint(shop_bp, url_prefix="/shop")
app.register_blueprint(basket_bp, url_prefix="/basket")
app.register_blueprint(home_bp, url_prefix="/home")
app.register_blueprint(checkout_bp, url_prefix="/checkout")

@app.route('/')
def root():
    return redirect(url_for('home.home'))
