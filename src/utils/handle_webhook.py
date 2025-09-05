from ..queries.item import edit_item_stock, get_item
from flask import current_app
import stripe

"""
    Throws: ValueError
        if there isn't an item_id in the sessions metadata
        if any of the query functions used throw
"""
def checkout_completed(session_raw):
    session = stripe.checkout.Session.retrieve(
            session_raw['id'],
            expand=['line_items', 'line_items.data.price.product']
        )

    for item in session.line_items.data:
        item_id = item['price']['product']['metadata'].get('item_id')
        
        if not item_id:
            raise ValueError("No item id.")

        curr_stock = get_item(current_app.config.get('DB_SESSION'), item_id).stock
        new_stock = max(curr_stock - item['quantity'], 0)

        edit_item_stock(current_app.config.get('DB_SESSION'), item_id, new_stock)

        
