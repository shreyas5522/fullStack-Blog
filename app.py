from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

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


@app.route('/contact')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
