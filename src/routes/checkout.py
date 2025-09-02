from flask import Blueprint, render_template, abort, session, jsonify, current_app, url_for
from jinja2 import TemplateNotFound
import stripe
from ..queries.item import get_item, edit_item_stock

checkout_bp = Blueprint('checkout', __name__, template_folder='../templates')

@checkout_bp.route('/', methods=['GET'])
def checkout():
    try:
        return render_template("checkout.html", stripe_pub_key=current_app.config.get('STRIPE_PUB_KEY'))
    except TemplateNotFound:
        abort(404)

@checkout_bp.route('/success', methods=['GET'])
def checkout_success():
    try:
        if session.get('basket') is None:
            return redirect(url_for('shop.shop'))

        for item_id, q in session.get('basket'):
            try:
                item = get_item(current_app.config.get('DB_SESSION'), item_id)
                if not item:
                    print(f"[WARN]: /checkout/success -> item with id {item_id} doesn't exist")
                    continue

                edit_item_stock(current_app.config.get('DB_SESSION'), item_id, max(item.stock - q, 0))
            except ValueError as e:
                print(f"[ERROR]: /checkout/success -> item with id {item_id} raises ValueError: {e}.")

        session['basket'] = []

        return render_template("checkout_success.html")
    except TemplateNotFound:
        abort(404)


@checkout_bp.route('/create-session', methods=['GET'])
def create_checkout_session():
    basket = session.get('basket')
    if basket is None:
        return redirect(url_for('shop.shop'))

    line_items = []

    for item_id, q in basket:
        item = get_item(current_app.config.get('DB_SESSION'), item_id)

        new_quan = min(item.stock - q, q)
        if new_quan == 0:
            continue

        q = new_quan

        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': item.title,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': q,
        })

    stripe.api_key = current_app.config.get('STRIPE_PRIV_KEY');

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        ui_mode='embedded',
        return_url=url_for('checkout.checkout_success', _external=True)
    )
    
    return jsonify({'client_secret': checkout_session.client_secret}), 200



