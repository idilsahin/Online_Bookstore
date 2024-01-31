from flask import Flask, request, jsonify,Blueprint,render_template,redirect,url_for
from ..Utils.database import db
from ..models.book_model import Book
from ..models.shoppingcart_model import ShoppingCart
from flask_login import login_required, current_user


cardcontroller = Blueprint('cardcontroller', __name__)

@cardcontroller.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.form
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)  # default to 1 if not specified

    if not all([user_id, book_id]):
        return jsonify({"error": "Missing user_id or book_id"}), 400

    cart_item = ShoppingCart(user_id=user_id, book_id=book_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('bookcontroller.books'))

@cardcontroller.route('/cart/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    cart_items = ShoppingCart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 404

    cart_details = []
    for item in cart_items:
        book = Book.query.get(item.book_id)
        cart_details.append({
            "book_title": book.title,
            "quantity": item.quantity,
            "price_per_unit": book.price
        })

    return render_template("home.html",cart_details=cart_details, user=current_user)

@cardcontroller.route('/cart', methods=['GET'])
@login_required
def mycart():
    cart_items = ShoppingCart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 404

    cart_details = []
    total_price = 0  # Initialize total_price

    for item in cart_items:
        book = Book.query.get(item.book_id)
        subtotal = item.quantity * book.price  # Calculate subtotal for each item
        total_price += subtotal  # Update total_price
        cart_details.append({
            "book_title": book.title,
            "book_id": book.id,
            "quantity": item.quantity,
            "price_per_unit": book.price,
            "subtotal": subtotal  # Include subtotal in the dictionary
        })
    
    total_price = round(total_price, 2)
    return render_template("mycard.html", cart_details=cart_details, total_price=total_price, user=current_user)


def get_customers_cart():
    cart_items = ShoppingCart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 404

    cart_details = []
    total_price = 0  # Initialize total_price

    for item in cart_items:
        book = Book.query.get(item.book_id)
        subtotal = item.quantity * book.price  # Calculate subtotal for each item
        total_price += subtotal  # Update total_price
        cart_details.append({
            "book_title": book.title,
            "book_id": book.id,
            "quantity": item.quantity,
            "price_per_unit": book.price,
            "subtotal": subtotal  # Include subtotal in the dictionary
        })

    return cart_details, total_price


@cardcontroller.route('/cart/update', methods=['PUT'])
def update_cart():
    data = request.json
    cart_item_id = data.get('cart_item_id')
    new_quantity = data.get('quantity')

    if not all([cart_item_id, new_quantity]):
        return jsonify({"error": "Missing cart_item_id or quantity"}), 400

    cart_item = ShoppingCart.query.get_or_404(cart_item_id)
    cart_item.quantity = new_quantity
    db.session.commit()
    return jsonify({"message": "Cart updated successfully"}), 200

@cardcontroller.route('/cart/delete', methods=['POST'])
def delete_from_cart():
    data = request.form
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    #cart_item = ShoppingCart.query.get((user_id, book_id))
    cart_item = ShoppingCart.query.filter_by(user_id=user_id, book_id=book_id).first()

    if not cart_item:
        return jsonify({"error": "Missing cart_item_id"}), 400

    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cardcontroller.mycart'))
