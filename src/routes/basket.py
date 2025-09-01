from flask import Blueprint, render_template, abort, session, jsonify, current_app
from jinja2 import TemplateNotFound

from ..queries.item import get_item

basket_bp = Blueprint('basket', __name__, template_folder='../templates')

@basket_bp.route('/', methods=['GET'])
def basket():
    try:
        items = []
        print(session.get('basket'))
        if session.get('basket') is not None:
            for id in session.get('basket'):
                try:
                    items.append(get_item(current_app.config.get('DB_SESSION'), id))
                except ValueError:
                    pass # TODO: Log this probably deleted item
            items = [(x.img, x.title, x.price, x.id) for x in items]

        return render_template("basket.html", items=items, basket_t="current-tab")
    except TemplateNotFound:
        abort(404)


