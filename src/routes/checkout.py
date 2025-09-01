from flask import Blueprint, render_template, abort, session, jsonify
from jinja2 import TemplateNotFound

checkout_bp = Blueprint('checkout', __name__, template_folder='../templates')

@checkout_bp.route('/', methods=['GET'])
def checkout():
    try:
        items = []
        for id in session.get('basket'):
            try:
                pass
            except ValueError:
                pass # TODO: Log this probably deleted item

        return render_template("checkout.html", items=items)
    except TemplateNotFound:
        abort(404)


