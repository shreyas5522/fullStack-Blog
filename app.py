from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from datetime import datetime

from models import db, Contacts, Posts, User
import json, builtins, os

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = os.path.join('static', 'assets', 'img')
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']


db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'logout'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route('/post.html')
def post():
    return render_template('post.html', post=post)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        posts = Posts.query.all()
        return render_template('dashboard.html', username=current_user.username, posts=posts)
    else:
        if request.method == 'POST':
            app_username = request.form.get('usern')
            app_userpass = request.form.get('userpass')

            # Query the user from the database
            user = User.query.filter_by(username=app_username, password=app_userpass).first()
            if user:
                # Log the user in using Flask-Login's login_user function
                login_user(user)
                posts = Posts.query.all()
                return render_template('dashboard.html', username=app_username, posts=posts)
            else:
                # Invalid credentials, you might want to handle this case
                flash('Invalid username or password.', 'error')
        return render_template('login.html', params=params)
    
@app.route('/dashboard/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('dashboard_settings.html')  # Render settings form with password masking

    elif request.method == 'POST' and new_user:
  
        new_username = request.form.get('new_username')

        if new_username:
            new_password = request.form['new_password']
            new_password = request.form['new_password']            
        else:    
            current_password = request.form['current_password']
            new_user_password = request.form['new_password']
            confirm_newuser_password = request.form['confirm_password']
        
            if current_user.password != current_password:
                flash('Incorrect current password', 'error')
                return redirect(url_for('settings'))

            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return redirect(url_for('settings'))

            # Update the user's password directly
            current_user.password = new_password
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('dashboard')) 
    
    return 'Invalid request method', 405  

@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
@login_required  
def edit(sno):
    if request.method == 'POST':
        box_title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        slug = request.form.get('slug')
        content = request.form.get('content')
        img_file = request.form.get('img_file')
        date = datetime.now()
        author = current_user.username

        if sno == 'add':
            post = Posts(title=box_title, slug=slug, content=content, subtitle=subtitle, img_file=img_file, date=date, author=author)
            db.session.add(post)
        else:
            post = Posts.query.filter_by(sno=sno).first()
            post.title = box_title
            post.slug = slug
            post.content = content
            post.subtitle = subtitle
            post.author = author
            post.img_file = img_file
            post.date = date
        db.session.commit()
        return redirect(url_for('edit', sno=post.sno,post = post))  # Redirect to the edited post

    if sno == 'add':
        box_title = ''
        subtitle = ''
        slug = ''
        content = ''
        img_file = ''
    else:
        post = Posts.query.filter_by(sno=sno).first_or_404()  # Returns 404 if sno doesn't exist
        box_title = post.title
        subtitle = post.subtitle
        slug = post.slug
        content = post.content
        img_file = post.img_file
        
    post = Posts.query.filter_by(sno=sno).first()
    return render_template('edit.html',post=post, params=params, sno=sno, box_title=box_title, subtitle=subtitle, slug=slug, content=content, img_file=img_file)


@app.route('/edit/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Handle file upload here
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('upload'))
    else:
        return render_template('upload_form.html')
    
@app.route("/delete/<int:sno>", methods=['GET', 'POST'])
@login_required
def delete(sno):
    post = Posts.query.filter_by(sno=sno).first()  # Fetch the post with the given sno
    if not post:
        flash('Post not found!', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('delete.html', post=post)


@app.route('/logout')
def logout():
    logout_user()

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

if __name__ == '__main__':
    app.run(debug=True)
