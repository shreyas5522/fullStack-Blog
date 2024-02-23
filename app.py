from flask import Flask, Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import json
local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key_here'

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    __tablename__ = 'Contacts'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(120), unique=False, nullable=False)
    msg = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/post')
@app.route('/post.html')
def post():
    return render_template('post.html')


@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')



@app.route('/contact', methods=["GET", "POST"])
@app.route('/contact.html')
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Check if email already exists in the database
        existing_entry = Contacts.query.filter_by(email=email).first()
        if existing_entry:
            flash('Email already exists!', 'error')
        else:
            # Add entry to database
            entry = Contacts(name=name, phone_num=phone, msg=message, email=email)
            db.session.add(entry)
            db.session.commit()
            flash('Entry added successfully!', 'success')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)