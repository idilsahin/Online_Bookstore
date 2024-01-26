from flask import Flask, request, jsonify,Blueprint,render_template
from ..Utils.database import db
from ..models.book_model import Book # db, User, Book, Order, OrderDetail, Review, ShoppingCart, Wishlist
from flask_login import login_required, current_user

bookcontroller = Blueprint('bookcontroller', __name__)
# Book Controllers

@bookcontroller.route('/get-books')
def get_books():
   # books = Book.query.all()
    books = [
    {
        "title": "Aetherial Alchemy",
        "image_url": "/static/images/product-item6.jpg",
        "price": 870
    },
    {
        "title": "The Lost Labyrinth",
        "image_url": "/static/images/product-item7.jpg",
        "price": 870
    },
    {
        "title": "Crystal Caverns",
        "image_url": "/static/images/product-item8.jpg",
        "price": 870
    },
    {
        "title": "Scarlet Secrets",
        "image_url": "/static/images/product-item9.jpg",
        "price": 870
    },
    {
        "title": "Starry Horizons",
        "image_url": "/static/images/product-item10.jpg",
        "price": 870
    },
    {
        "title": "Dance of Fireflies",
        "image_url": "/static/images/product-item2.jpg",
        "price": 870
    },
    {
        "title": "Siren's Song",
        "image_url": "/static/images/product-item4.jpg",
        "price": 870
    },
    {
        "title": "Misty Mirage",
        "image_url": "/static/images/product-item3.jpg",
        "price": 870
    }
    ]
    book_list = [{'title': book['title'], 'price': book['price'], 'image_url': book['image_url']} for book in books]
    print(book_list)
    return render_template('recommended.html', books=book_list, user=current_user)

@bookcontroller.route('/book', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(
        title=data.get('title'),
        author=data.get('author'),
        isbn=data.get('isbn'),
        publisher=data.get('publisher'),
        publication_year=data.get('publication_year'),
        category=data.get('category'),
        price=data.get('price'),
        stock_quantity=data.get('stock_quantity'),
        description=data.get('description'),
        cover_image=data.get('cover_image')
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created successfully", "book_id": new_book.id}), 201

@bookcontroller.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    book_data = {
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        # ... include other fields as needed
    }
    return jsonify(book_data), 200

@bookcontroller.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    # ... update other fields as needed
    db.session.commit()
    return jsonify({"message": "Book updated successfully"}), 200

@bookcontroller.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200