from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

home_bp = Blueprint('home', __name__, template_folder='../templates')

@home_bp.route('/')
def home():
    try:
        return render_template("home.html", home_t="current-tab")
    except TemplateNotFound:
        abort(404)
