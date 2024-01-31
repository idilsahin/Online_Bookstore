
from flask import Flask, request, jsonify,Blueprint,render_template
from ..Utils.database import db
from ..models.order_model import Order # db, User, Book, Order, OrderDetail, Review, ShoppingCart, Wishlist
from ..models.order_details_model import OrderDetail
from ..models.book_model import Book
from ..controllers.cardcontroller import get_customers_cart
from ..controllers.usercontroller import get_user
from flask_login import login_required, current_user
from datetime import datetime

ordercontroller = Blueprint('ordercontroller', __name__)
# Book Controllers
#@ordercontroller.route('/order', methods=['POST'])
@ordercontroller.route('/create_order', methods=['GET', 'POST'])
def create_order():
    
    order_details,total_price = get_customers_cart()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_status_options = ["Pending", "Processing", "Shipped", "Delivered"]
    if request.method == 'POST':
        # Retrieve data from the form submission
        user_id = request.form.get('user_id')
        total_price = request.form.get('total_price')
        order_date = datetime.strptime(request.form.get('order_date'), '%Y-%m-%d %H:%M:%S')
        shipping_address = request.form.get('shipping_address')
        status = request.form.get('status')
        payment_method = request.form.get('payment_method')        

                # Create an instance of the Order model
        order = Order(
            user_id=user_id,
            total_price=total_price,
            order_date=order_date,
            shipping_address=shipping_address,
            status="Processing",
            payment_method=payment_method
        )
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID

        

        for detail in order_details:
            book_id = detail.get('book_id')
            quantity = detail.get('quantity')
            price_per_unit = detail.get('price_per_unit')

            if not all([book_id, quantity, price_per_unit]):
                return jsonify({"error": "Missing order detail information"}), 400

            order_detail = OrderDetail(order_id=order.id, book_id=book_id, quantity=quantity, price_per_unit=price_per_unit)
            db.session.add(order_detail)

        db.session.commit()
        
        return jsonify({"message": "Order created successfully", "order_id": order.id}), 201
    
    return render_template('ordermanagement.html', cart_details=order_details, total_price=total_price,current_date=current_date, user=current_user)  # Render the form on GET request        


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

@ordercontroller.route('/admin/search', methods=['GET', 'POST'])
def search_orders():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        userinfo = get_user(user_id)

        if userinfo:
            orders = Order.query.filter_by(user_id=user_id).all()
            return render_template('customerorders.html',user=current_user, orders=orders)
        else:
            return render_template('customerorders.html',  user=current_user, orders=None)

    return render_template('customerorders.html', user=current_user)