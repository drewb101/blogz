from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'suerSecretBlogz'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    created = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.created = datetime.now()

    def is_valid(self):
        if self.title and self.body and self.created:
            return True
        else:
            return False


@app.route("/")
def index():
    return redirect("/blog")


@app.route("/blog")
def display_blog_blogs():

    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('single_blog.html', title="Blog Blog",
                               blog=blog)

    sort = request.args.get('sort')
    if (sort == "newest"):
        all_blogs = Blog.query.order_by(Blog.created.desc()).all()
    else:
        all_blogs = Blog.query.all()
    return render_template('all_blogs.html', title="All Blog Posts",
                           all_blogs=all_blogs)


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
                               title="Create new blog blog")


if __name__ == '__main__':
    app.run()
