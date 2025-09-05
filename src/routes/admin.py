from flask import Blueprint, render_template, abort, request, jsonify, current_app, session, redirect, url_for
from jinja2 import TemplateNotFound
from ..utils.generation import generate_safe_image
from ..queries.admin import check_admin_credentials
from ..queries import item
import os

admin_bp = Blueprint('admin', __name__, template_folder="../templates")

@admin_bp.route('/')
def dash():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    items = []

    try:
        items = item.get_items(current_app.config.get('DB_SESSION'))
        items = [(x.img, x.title, x.price, x.id, x.stock) for x in items]
    except ValueError as e:
        print(e)

    try:
        return render_template('admin/dash.html', items=items, dash_t="current-tab")
    except TemplateNotFound:
        abort(404)

@admin_bp.route('/logout', methods=['GET'])
def logout():
    if session.get('admin_logged_in'):
        session.pop('admin_logged_in', None)

    return redirect(url_for('home.home'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if session.get('admin_logged_in'):
            return jsonify({'error': 'You are already logged in. Go to /admin/'}), 418

        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'error': 'You must provide a username and password'}), 400

        if not check_admin_credentials(current_app.config.get('DB_SESSION'), username, password):
            return jsonify({'error': 'Invalid password'}), 401
        
        session['admin_logged_in'] = True
        return jsonify({'success': 'Logged in successfully'}), 200


    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dash'))

    try:
        return render_template('admin/login.html')
    except TemplateNotFound:
        abort(404)

@admin_bp.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'You must be admin to post items'}), 401

        price = request.form.get('price')
        title = request.form.get('title')
        stock = request.form.get('stock')

        if price is None or title is None or stock is None:
            return jsonify({'error': 'You must provide a price, title and stock'}), 400

        img = request.files['img']

        if img is None or img.filename == '':
            return jsonify({'error': 'You must provide an image'}), 400

        tmp_img = os.path.join(current_app.config.get('TMP_IMAGE_FOLDER'), img.filename)
        img.save(tmp_img)

        try:
            img_path = generate_safe_image(tmp_img, remove=True)
        except ValueError as e:
            return jsonify({'error': 'Image could not be saved'}), 400

        try:
            item.create_item(current_app.config.get('DB_SESSION'), title, img_path, price, stock)
        except ValueError:
            print(f"[ERROR]: /admin/add_item -> Failed to create item. Err: {e}")
            return jsonify({'error': f'Failed to create item'}), 400

        return jsonify({'success': 'Image uploaded successfully.'}), 200

    try:
        return render_template('admin/add_item.html', add_item_t="current-tab")
    except TemplateNotFound:
        abort(404)

@admin_bp.route('/delete-item', methods=['POST'])
def delete_item():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'You must be admin to delete items'}), 401

    item_id = request.form.get('id')
    
    try:
        item.delete_item(current_app.config.get('DB_SESSION'), item_id)
    except ValueError as e:
        print(f"[ERROR]: /admin/delete_item -> Failed to delete item. Err: {e}")
        return jsonify({'error': f'Failed to delete item.'}), 400

    return jsonify({'success': 'Successfully deleted image.'}), 200

@admin_bp.route('/update-item', methods=['POST'])
def update_item():
    item_id = request.form.get('item_id')
    new_title = request.form.get('title')
    new_stock = request.form.get('stock')
    new_price = request.form.get('price')

    db_session = current_app.config.get('DB_SESSION')
    try:
        item.update_item(db_session, item_id, new_title, int(new_stock), float(new_price))
    except (ValueError, TypeError) as e:
        print(f"[ERROR]: /admin/update-item -> Failed to update item. Err: {e}")
        return jsonify({'error': 'Failed to delete item'}), 400
    
    return jsonify({'success': 'Updated item successfully'}), 200
            


