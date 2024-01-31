from flask_login import UserMixin
from ..Utils.database import db
from datetime import datetime

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20), unique=True)
    publisher = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    category = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock_quantity = db.Column(db.Integer)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    cuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    cdate = db.Column(db.DateTime, default=datetime.utcnow)
    uuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    udate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

        # Relationships
   #  order_details = db.relationship('OrderDetail', backref='book', lazy=True)
   #  reviews = db.relationship('Review', backref='book', lazy=True)
    # cart_items = db.relationship('ShoppingCart', backref='book', lazy=True)
   #  wishlist_items = db.relationship('Wishlist', backref='book', lazy=True)