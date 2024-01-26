from flask_login import UserMixin
from ..Utils.database import db
from datetime import datetime
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    review_date = db.Column(db.DateTime)
    cuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    cdate = db.Column(db.DateTime, default=datetime.utcnow)
    uuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    udate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
