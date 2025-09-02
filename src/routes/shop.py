from flask import Blueprint, render_template, abort, session, jsonify, request, current_app
from jinja2 import TemplateNotFound

from ..queries.item import get_items, isitem

shop_bp = Blueprint('shop', __name__, template_folder='../templates')

@shop_bp.route('/', methods=['GET', 'POST'])
def shop():
    # Add to basket
    if request.method == "POST": 
        if session.get('basket') is None:
            session['basket'] = []
        item_id = request.form.get('item_id')
        try:
            if not isitem(current_app.config.get('DB_SESSION'), item_id):
                return jsonify({'error': 'Item does not exist'}), 400

        except ValueError as e:
            return jsonify({'error': e}), 400

        basket = session.get('basket', [])
        found = False

        for i, (id, q) in enumerate(basket):
            if id == item_id:
                basket[i] = (id, q + 1)
                found = True
                break

        if not found:
            basket.append((item_id, 1))

        session['basket'] = basket
        
        return jsonify({'success', 'item added to basket'}), 200

    items = []

    try:
        items = get_items(current_app.config.get('DB_SESSION'))
        items = [(x.img, x.title, x.price, x.id, x.stock) for x in items]
    except ValueError as e:
        print(e)
        return redirect(url_for('home.home'))
        
    try:
        return render_template("shop.html", items=items, shop_t="current-tab")
    except TemplateNotFound:
        abort(404)

