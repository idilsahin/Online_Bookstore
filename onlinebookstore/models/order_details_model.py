from flask_login import UserMixin
from ..Utils.database import db
from datetime import datetime
class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer)
    price_per_unit = db.Column(db.Float)
    cuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    cdate = db.Column(db.DateTime, default=datetime.utcnow)
    uuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    udate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    