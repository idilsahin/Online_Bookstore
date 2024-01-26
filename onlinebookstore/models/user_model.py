from flask_login import UserMixin
from ..Utils.database import db
from datetime import datetime
# Define the User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    cuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    cdate = db.Column(db.DateTime, default=datetime.utcnow)
    uuser = db.Column(db.Integer, db.ForeignKey('user.id'))
    udate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class FavoriteBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)