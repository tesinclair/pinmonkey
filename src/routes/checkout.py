from flask import Blueprint, render_template, abort, session, jsonify, current_app, url_for, redirect
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

        q = min(item.stock, q)
        if q <= 0:
            continue

        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': item.title,
                    'metadata': {
                        'item_id': item.id
                    }
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': q,
        })

    if len(line_items) <= 0:
        print(f"[WARN]: /checkout/create-session -> No line items. Info:\n\tItem -> {item.title}\n\tStock -> {item.stock}\n\tQuantity -> {q}")
        return jsonify({'error': 'No items in basket'}), 400

    stripe.api_key = current_app.config.get('STRIPE_PRIV_KEY');

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        ui_mode='embedded',
        return_url=url_for('checkout.checkout_success', _external=True)
    )
    
    return jsonify({'client_secret': checkout_session.client_secret}), 200



