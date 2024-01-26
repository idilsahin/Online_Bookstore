
from flask import Flask, request, jsonify,Blueprint
from ..Utils.database import db
from ..models.book_model import Book
from ..models.wishlist_model import Wishlist
from ..models.user_model import User,FavoriteBooks

usercontroller = Blueprint('usercontroller', __name__)

@usercontroller.route('/favorite', methods=['POST'])
def add_to_favorites():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    if not all([user_id, book_id]):
        return jsonify({"error": "Missing user_id or book_id"}), 400

    favorite = FavoriteBooks(user_id=user_id, book_id=book_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Book added to favorites successfully"}), 201

@usercontroller.route('/favorite/<int:user_id>', methods=['GET'])
def view_favorites(user_id):
    favorites = FavoriteBooks.query.filter_by(user_id=user_id).all()

    if not favorites:
        return jsonify({"message": "No favorite books found"}), 404

    favorite_books = []
    for favorite in favorites:
        book = Book.query.get(favorite.book_id)
        favorite_books.append({
            "book_id": book.id,
            "book_title": book.title
        })

    return jsonify(favorite_books), 200

@usercontroller.route('/favorite/delete', methods=['DELETE'])
def remove_from_favorites():
    data = request.json
    favorite_id = data.get('favorite_id')

    if not favorite_id:
        return jsonify({"error": "Missing favorite_id"}), 400

    favorite = FavoriteBooks.query.get_or_404(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Book removed from favorites successfully"}), 200