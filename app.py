from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from models import db, Contacts, Posts, User
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
    if 'user' in session:
        username = session['user']
        posts = Posts.query.all()
        return render_template('dashboard.html', username=username, posts=posts)

    if request.method == 'POST':
        app_username = request.form.get('usern')
        app_userpass = request.form.get('userpass')
        if (app_username == params['username'] and app_userpass == params['password']):
            session['user'] = app_username
            posts = Posts.query.all()
            return render_template('dashboard.html', username=app_username, posts=posts)
        else:
            # Invalid credentials, you might want to handle this case
            return render_template('login.html', params=params)
    
    # Render login.html if GET and user is not logged in.
    return render_template('login.html', params=params)



#If want to create login for loginPage and dashboard for dashboard page
# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     if 'user' in session and session['user'] == params['username']:
#         return render_template('dashboard.html', username=session.get('username'))
#     else:
#         # If user is not logged in, redirect to login
#         return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('username', None)
    return redirect(url_for('dashboard'))

    
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

# @app.route('/edit/<string:no>', methods=["GET", "POST"])
# def edit(sno):
#     if ('user' in session and session['user'] == params['admin_user']):

if __name__ == '__main__':
    app.run(debug=True)
