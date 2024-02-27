from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import json
from models import db, Contacts, Posts
import builtins

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key_here'

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db.init_app(app)

@app.route('/')
@app.route('/index.html')
def index():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params = params, posts=posts)

@app.route('/post/<string:post_slug>',methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route('/post.html')
def post():
    return render_template('post.html', post = post)

@app.route('/dashboard')
def dashboard():
    return render_template('login.html', post = post)


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

        existing_entry = Contacts.query.filter_by(email=email).first()
        if existing_entry:
            flash('Email already exists!', 'error')
        else:
            entry = Contacts(name=name, phone_num=phone, msg=message, email=email)
            db.session.add(entry)
            db.session.commit()
            flash('Entry added successfully!', 'success')

    return render_template('contact.html', builtins=builtins)

if __name__ == '__main__':
    app.run(debug=True)
