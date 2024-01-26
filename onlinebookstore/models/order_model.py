from flask_login import UserMixin
from ..Utils.database import db
from datetime import datetime


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float)
    order_date = db.Column(db.DateTime)
    shipping_address = db.Column(db.String(200))
    status = db.Column(db.String(50))
    payment_method = db.Column(db.String(50))
    tracking_number = db.Column(db.String(100))
    # Relationships
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)
    cuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    cdate = db.Column(db.DateTime, default=datetime.utcnow)
    uuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    udate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)