from flask import Flask, redirect, url_for, session, request
from .extensions import db_init
from .routes.shop import shop_bp
from .routes.basket import basket_bp 
from .routes.home import home_bp
from .routes.checkout import checkout_bp
from .routes.admin import admin_bp
from .commands.seed import cli_tools_seed
from .commands.create_admin import cli_tools_create_admin
from .commands.remove_admin import cli_tools_remove_admin
from .utils import handle_webhook
import stripe

from dotenv import dotenv_values
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
os.makedirs(IMAGE_FOLDER, exist_ok=True)

TMP_IMAGE_FOLDER = os.path.join(BASE_DIR, 'tmp', 'images')
os.makedirs(TMP_IMAGE_FOLDER, exist_ok=True)

DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'pinmonkey.db')

PM_CONF = dotenv_values('../pinmonkey.env')

SECRET_KEY = PM_CONF.get('PM_FLASK_SECRET')
STRIPE_SECRET_KEY = PM_CONF.get('PM_STRIPE_SECRET')
STRIPE_PUB_KEY = PM_CONF.get('PM_STRIPE_PUB_KEY')
STRIPE_WHSEC = PM_CONF.get('PM_STRIPE_WHSEC')

if not SECRET_KEY or not STRIPE_SECRET_KEY or not STRIPE_PUB_KEY or not STRIPE_WHSEC:
    print("ERROR: A config variable is not set!")
    sys.exit(1)

app = Flask(__name__, static_folder='static')

# Secrets
app.config['SECRET_KEY'] = SECRET_KEY
app.config['STRIPE_PRIV_KEY'] = STRIPE_SECRET_KEY
app.config['STRIPE_PUB_KEY'] = STRIPE_PUB_KEY
app.config['STRIPE_WHSEC'] = STRIPE_WHSEC

# Utils
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['TMP_IMAGE_FOLDER'] = TMP_IMAGE_FOLDER
app.config['DB_SESSION'], app.config['DB_ENGINE'] = db_init(DATABASE_URL)

app.register_blueprint(shop_bp, url_prefix="/shop")
app.register_blueprint(basket_bp, url_prefix="/basket")
app.register_blueprint(home_bp, url_prefix="/home")
app.register_blueprint(checkout_bp, url_prefix="/checkout")
app.register_blueprint(admin_bp, url_prefix="/admin")

app.cli.add_command(cli_tools_seed)
app.cli.add_command(cli_tools_create_admin)
app.cli.add_command(cli_tools_remove_admin)


@app.route('/')
def root():
    session['basket'] = []
    return redirect(url_for('home.home'))

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    req = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    event = stripe.Webhook.construct_event(
            req, sig_header, app.config.get('STRIPE_WHSEC')
        )

    if event['type'] == 'checkout.session.completed':
        try:
            handle_webhook.checkout_completed(event['data']['object'])
        except ValueError as e:
            print(f"[ERROR]: /stripe-webhook -> in: handle_webhook.checkout_completed. Err: {e}")

    return '', 200
