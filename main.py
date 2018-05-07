from flask import Flask, request, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'superSecretBlogzKey'


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.user = user
        self.created = datetime.now()

    def is_valid(self):
        if self.title and self.body and self.user and self.created:
            return True
        else:
            return False


@app.before_request
def require_login():
    allowed_routes = ['index', 'static',
                      'login', 'list_blogs', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not username and not password:
            flash("Username and password cannot be blank")
            return render_template('login.html')
        if not password:
            flash("Invalid password")
            return render_template('login.html')
        if not username:
            flash("Invalid username")
            return render_template('login.html')

        if user and user.password == password:
            session['username'] = username
            flash("Successful login")
            return redirect('/newpost')
        if user and not user.password == password:
            flash("Invalid password")
            return render_template('login.html')
        if not user:
            flash("THat login does not exist.")
            return render_template('login.html')

    else:
        return render_template('login.html')


@app.route("/")
def index():
    users = User.query.all()
    return render_template("/index.html", users=users)


@app.route("/blog", methods=['POST', 'GET'])
def all_blogs():
    blog_id = request.args.get('id')
    user_id = request.args.get('user_id')
    blogs = Blog.query.order_by(Blog.created.desc())

    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('single_blog.html', title="Blog",
                               blog=blog)

    if (user_id):
        user_blog = Blog.query.filter_by(user_id=author_id)
        return render_template('single_blog.html', blogs=author_blog)

    return render_template('all_blogs.html', title="All Blog Posts",
                           blogs=all_blogs)


@app.route('/newpost', methods=['GET', 'POST'])
def new_blog():
    if request.method == 'POST':
        new_blog_title = request.form['title']
        new_blog_body = request.form['body']
        new_blog = Blog(new_blog_title, new_blog_body)

        if new_blog.is_valid():
            db.session.add(new_blog)
            db.session.commit()

            url = "/blog?id=" + str(new_blog.id)
            return redirect(url)
        else:
            flash("""Please check your blog for errors. Both a title
            and a body are required.""")
            return render_template('new_blog_form.html',
                                   title="Add a Blog Entry",
                                   new_blog_title=new_blog_title,
                                   new_blog_body=new_blog_body)

    else:
        return render_template('new_blog_form.html',
                               title="Create new blog")


if __name__ == '__main__':
    app.run()
