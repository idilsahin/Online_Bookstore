from flask import Flask, request, jsonify,Blueprint
from ..Utils.database import db
from ..models.book_model import Book
from ..models.wishlist_model import Wishlist

wishlistcontroller = Blueprint('wishlistcontroller', __name__)

@wishlistcontroller.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    if not all([user_id, book_id]):
        return jsonify({"error": "Missing user_id or book_id"}), 400

    wishlist_item = Wishlist(user_id=user_id, book_id=book_id)
    db.session.add(wishlist_item)
    db.session.commit()
    return jsonify({"message": "Item added to wishlist successfully"}), 201

@wishlistcontroller.route('/wishlist/<int:user_id>', methods=['GET'])
def view_wishlist(user_id):
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()

    if not wishlist_items:
        return jsonify({"message": "Wishlist is empty"}), 404

    wishlist_details = []
    for item in wishlist_items:
        book = Book.query.get(item.book_id)
        wishlist_details.append({
            "book_id": book.id,
            "book_title": book.title
        })

    return jsonify(wishlist_details), 200

@wishlistcontroller.route('/wishlist/delete', methods=['DELETE'])
def delete_from_wishlist():
    data = request.json
    wishlist_item_id = data.get('wishlist_item_id')

    if not wishlist_item_id:
        return jsonify({"error": "Missing wishlist_item_id"}), 400

    wishlist_item = Wishlist.query.get_or_404(wishlist_item_id)
    db.session.delete(wishlist_item)
    db.session.commit()
    return jsonify({"message": "Item removed from wishlist successfully"}), 200