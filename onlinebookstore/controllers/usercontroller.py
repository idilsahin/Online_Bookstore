
from flask import Flask, request, jsonify,Blueprint,render_template,redirect,url_for
from ..Utils.database import db
from ..models.book_model import Book
from ..models.wishlist_model import Wishlist
from ..models.user_model import User,FavoriteBooks
from flask_login import login_required, current_user

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

@usercontroller.route('/usermanagement')
def usermanagement():
    users = User.query.all()
    return render_template('usermanagement.html', users=users,  user=current_user)


@usercontroller.route('/get_user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'password': user.password,  # Note: You might want to exclude the password from the response
            'role_id': user.role_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@usercontroller.route('/createuser', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = int(request.form['role_id'])
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        new_user = User(
            username=username,
            password=password,
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('usercontroller.usermanagement'))
    return render_template('createuser.html')

@usercontroller.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.role_id = int(request.form['role_id'])
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', user=user)

@usercontroller.route('/deleteuser/<int:id>', methods=['POST'])
def deleteuser(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})