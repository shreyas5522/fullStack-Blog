from flask import Flask, render_template, request, flash, session, redirect, url_for
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

from flask import session, redirect, url_for, request, render_template

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == session.get('username'):
        return render_template('dashboard.html', params=session.get('username'))

    if request.method == 'POST':
        username = request.form.get('username')
        userpass = request.form.get('userpass')
        if username == params['username'] and userpass == params['password']:
            session['user'] = username
            session['username'] = username
            return render_template('dashboard.html', params=params)
        else:
            # If username or password is incorrect, render login template
            return render_template('login.html', params=params)

    # If request method is GET and user is not logged in, redirect to login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', params=params)
    elif request.method == 'POST':
        # Handle login form submission
        username = request.form.get('username')
        userpass = request.form.get('userpass')
        if username == params['username'] and userpass == params['password']:
            session['user'] = username
            session['username'] = username
            return redirect(url_for('dashboard', params=params))
        else:
            # If username or password is incorrect, render login template with error message
            return render_template('login.html', error="Invalid username or password.", params=params)

    
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
