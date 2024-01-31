from flask import Flask, request, jsonify,Blueprint,render_template,abort,render_template_string,flash,redirect,url_for
from ..Utils.database import db
from ..models.book_model import Book # db, User, Book, Order, OrderDetail, Review, ShoppingCart, Wishlist
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

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

@bookcontroller.route('/productmanagement')
def index():
    return render_template('productmanagement.html',  user=current_user)

@bookcontroller.route('/books')
def books():
    # Fetch books from the database
    books = Book.query.all()
    return render_template('books.html', books=books,  user=current_user)

@bookcontroller.route("/book/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    if book is None:
        abort(404)
    return render_template('book.html', book=book,  user=current_user)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@bookcontroller.route('/create_book', methods=['POST'])
def create_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    publisher = request.form.get('publisher')
    publication_year = request.form.get('publication_year')
    category = request.form.get('category')
    price = request.form.get('price')
    stock_quantity = request.form.get('stock_quantity')
    description = request.form.get('description')
    
    # Handle cover image upload
    cover_image = request.files['cover_image']
    if cover_image and allowed_file(cover_image.filename):
        filename = secure_filename(cover_image.filename)
        cover_image.save(os.path.join(os.getcwd(), 'Online_Bookstore','onlinebookstore', 'static', 'images', filename))
        #cover_image.save(os.path.join('onlinebookstore\\static\\images', filename))
    else:
        filename = None  # Set to default image or handle as needed

    new_book = Book(
        title=title,
        author=author,
        isbn=isbn,
        publisher=publisher,
        publication_year=publication_year,
        category=category,
        price=price,
        stock_quantity=stock_quantity,
        description=description,
        cover_image=filename
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully'})

@bookcontroller.route('/book2/<int:book_id>', methods=['GET'])
def get_book2(book_id):
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

@bookcontroller.route('/search_book', methods=['GET'])
def search_book():
    query = request.args.get('query')

    if not query:
        return jsonify({'error': 'No search query provided'}), 400

    # Perform a case-insensitive search on title, author, or book id
    results = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) |
        (Book.author.ilike(f'%{query}%')) |
        (Book.id == query)
    ).all()

    return render_template('productmanagement.html', user=current_user ,results=results, search_query=query)

