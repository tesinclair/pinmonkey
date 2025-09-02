from flask import Blueprint, render_template, abort, session, jsonify, current_app, request
from jinja2 import TemplateNotFound

from ..queries.item import get_item

basket_bp = Blueprint('basket', __name__, template_folder='../templates')

@basket_bp.route('/', methods=['GET', 'POST'])
def basket():
    if request.method == 'POST':
        new_quantity = request.form.get('new_quantity')
        item_id = request.form.get('item_id')

        if new_quantity is None or item_id is None:
            return jsonify({'error': 'You need to provide a new quantity and an item id'}), 400

        basket = session.get('basket', [])
        found = False
        for i, (id, _) in enumerate(basket):
            if id == item_id:
                basket[i] = (id, int(new_quantity))
                found = True
                break

        if not found:
            return jsonify({'error': 'Item not found in basket'}), 400

        session['basket'] = basket
        session.modified = True

        return jsonify({'success': 'Basket updated'}), 200

    try:
        items = []
        print(session.get('basket'))
        if session.get('basket') is not None:
            for id, quantity in session.get('basket'):
                try:
                    items.append(get_item(current_app.config.get('DB_SESSION'), id))
                except ValueError:
                    pass # TODO: Log this probably deleted item
            items = [(x.img, x.title, x.price, x.id, quantity) for x in items]

        return render_template("basket.html", items=items, basket_t="current-tab")
    except TemplateNotFound:
        abort(404)

@basket_bp.route('/remove', methods=['POST'])
def basket_remove():
    item_id = request.form.get('item_id')

    if item_id is None:
        return jsonify({'error': 'You must provide an item id'}), 400

    basket = session.get('basket', [])
    found = False
    for i, (id, _) in enumerate(basket):
        if id == item_id:
            basket.pop(i)
            found = True
            break

    if not found:
        return jsonify({'error': 'Item not found in basket'}), 400

    session['basket'] = basket
    session.modified = True

    return jsonify({'success': 'item removed'}), 200


