from App.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64),nullable=False,unique=True)
    password = db.Column(db.String(128),nullable=False)
    gender = db.Column(db.String(8),nullable=False,default="male")
    email = db.Column(db.String(128),nullable=False)
    age = db.Column(db.Integer,nullable=False,default=18)
    is_active = db.Column(db.Boolean,nullable=False,default=False)
    tokon = db.Column(db.String(128), nullable=False)
    permission = db.Column(db.Integer,nullable=False,default=0)