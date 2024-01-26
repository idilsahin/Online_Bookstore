
from flask import Flask, request, jsonify,Blueprint
from ..Utils.database import db
from ..models.order_model import Order # db, User, Book, Order, OrderDetail, Review, ShoppingCart, Wishlist
from ..models.order_details_model import OrderDetail
from ..models.book_model import Book

ordercontroller = Blueprint('ordercontroller', __name__)
# Book Controllers
@ordercontroller.route('/order', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    order_details = data.get('order_details')  # This should be a list of dictionaries

    if not user_id or not order_details:
        return jsonify({"error": "Missing user_id or order_details"}), 400

    new_order = Order(user_id=user_id)
    db.session.add(new_order)
    db.session.flush()  # Flush to get the order ID

    for detail in order_details:
        book_id = detail.get('book_id')
        quantity = detail.get('quantity')
        price_per_unit = detail.get('price_per_unit')

        if not all([book_id, quantity, price_per_unit]):
            return jsonify({"error": "Missing order detail information"}), 400

        order_detail = OrderDetail(order_id=new_order.id, book_id=book_id, quantity=quantity, price_per_unit=price_per_unit)
        db.session.add(order_detail)

    db.session.commit()
    return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201

@ordercontroller.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    order_details = OrderDetail.query.filter_by(order_id=order.id).all()
    
    details = []
    for detail in order_details:
        book = Book.query.get(detail.book_id)
        details.append({
            "book_title": book.title,
            "quantity": detail.quantity,
            "price_per_unit": detail.price_per_unit
        })

    order_data = {
        "user_id": order.user_id,
        "order_date": order.order_date,
        "order_details": details
    }
    return jsonify(order_data), 200

@ordercontroller.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json
    status = data.get('status')
    
    if status:
        order.status = status
        db.session.commit()
        return jsonify({"message": "Order updated successfully"}), 200
    else:
        return jsonify({"error": "No update information provided"}), 400

@ordercontroller.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"}), 200