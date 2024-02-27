from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contacts(db.Model):
    __tablename__ = 'Contacts'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(120), unique=False, nullable=False)
    msg = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Posts(db.Model):
    __tablename__ = 'posts'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug  = db.Column(db.String(12), unique=False, nullable=False)
    content = db.Column(db.String(2500), unique=False, nullable=False)
    subtitle = db.Column(db.String(50), unique=False, nullable=False)
    author = db.Column(db.String(12), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=True, nullable=True)
    img_file = db.Column(db.String(12), nullable=True)