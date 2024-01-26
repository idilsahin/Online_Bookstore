from flask import Flask, request, jsonify,Blueprint
from ..Utils.database import db
from ..models.book_model import Book
from ..models.shoppingcart_model import ShoppingCart

cardcontroller = Blueprint('cardcontroller', __name__)

@cardcontroller.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)  # default to 1 if not specified

    if not all([user_id, book_id]):
        return jsonify({"error": "Missing user_id or book_id"}), 400

    cart_item = ShoppingCart(user_id=user_id, book_id=book_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Item added to cart successfully"}), 201

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

    return jsonify(cart_details), 200

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

@cardcontroller.route('/cart/delete', methods=['DELETE'])
def delete_from_cart():
    data = request.json
    cart_item_id = data.get('cart_item_id')

    if not cart_item_id:
        return jsonify({"error": "Missing cart_item_id"}), 400

    cart_item = ShoppingCart.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Item removed from cart successfully"}), 200
