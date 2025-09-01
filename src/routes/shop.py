from flask import Blueprint, render_template, abort, session, jsonify, request, current_app
from jinja2 import TemplateNotFound

from ..queries.item import get_items, isitem

shop_bp = Blueprint('shop', __name__, template_folder='../templates')

@shop_bp.route('/', methods=['GET', 'POST'])
def shop():
    # Add to basket
    if request.method == "POST": 
        item_id = request.form.get('item_id')
        try:
            if not isitem(current_app.config.get('DB_SESSION'), item_id):
                return jsonify({'error': 'Item does not exist'}), 400
        except ValueError as e:
            return jsonify({'error': e}), 400

        session['basket'] = session.get('basket').append(item_id)
        
    try:
        return render_template("shop.html", items=get_items(current_app.config.get('DB_SESSION')), shop_t="current-tab")
    except TemplateNotFound:
        abort(404)

