from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1. Lallllllaaa',
        'author': 'Aaron'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2. gggallllllaaa'
    },
    {
        'title': 'Post 3',
        'content': 'This is the content of post 3. jjjallllllaaa'
    },
]


@app.route('/')
# @app.route('/home/<string:name>')
def hello():
    # return "Hello " + name
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author='Aaron')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/onlyget', methods=['GET'])
def only_get():
    return "Only respond to get request"


if __name__ == "__main__":
    app.run(debug=True)
