from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from forms import RegistrationForm, PostForm
import os

app = Flask(__name__)

# DB connection
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_PASSWORD'] = os.environ['mysqlpass']
app.config['MYSQL_DB'] = 'testing'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


posts = [
    {
        'id': 1,
        'author': 'Rav',
        'title': 'Hello World',
        'created_at': 'May 16, 2018',
        'post_content': 'Welcome to BioHack 2018'
    },
    {
        'id': 2,
        'author': 'Alice',
        'title': 'Flask Tutorial',
        'created_at': 'May 18, 2018',
        'post_content': 'Flask is awesome'
    },
]


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/home')
@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        result = create_user(username, email, password)
        if result:
            flash('Registration Successful', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM user WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM article")

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

@app.route('/articles')
def articles():

     # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM article")

    articles = cur.fetchall()
    cur.close()
    if result > 0:

        return render_template('articles.html', result=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)

@app.route('/post/<string:id>')
def get_post(id):
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM article WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('post.html', post=article)

# Add Article
@app.route('/add_post', methods=['GET', 'POST'])
@is_logged_in
def add_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO article(title, content, author) VALUES(%s, %s, %s)",(title, content, session['username']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Post Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_post.html', form=form)




# URL variables:
@app.route('/user/<username>')
def show_profile(username):
    return 'Welcome %s' % username.capitalize()

def create_user(username, email, password):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute query
    cur.execute("INSERT INTO user(email, username, password) VALUES(%s, %s, %s)", (email, username, password))

    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    return True



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, port=9999)
