from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///postdata.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        dead_line_check(Post.query.all())
        posts = Post.query.order_by(Post.post_date).all()
        return render_template('home.html', posts=posts)
    else:
        try:
            user = request.form.get('user')
            title = request.form.get('title')
            detail = request.form.get('detail')
            post_date = request.form.get('post_date')

            post_date = datetime.strptime(post_date, '%Y-%m-%d')
            new_post = Post(user=user, title=title, detail=detail, post_date=post_date)
        except ValueError as e:
            print("Error : ", e)
            return redirect('/create')
        else:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/edit/<int:id>')
def edit(id):
    post = Post.query.get(id)
    return render_template('edit.html', post=post)

@app.route('/commit/<int:id>', methods=['GET', 'POST'])
def commit(id):
    try:
        com_post = Post.query.get(id)
        com_post.user = request.form.get('user')
        com_post.title = request.form.get('title')
        com_post.detail = request.form.get('detail')
        date = request.form.get('post_date')
        com_post.post_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError as e:
        print("Error : ", e)
        return redirect('/edit/'+id)
    else:
        db.session.merge(com_post)
        db.session.commit()
        return redirect('/')

@app.route('/detail/<int:id>')
def detail(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/deleteConf/<int:id>')
def deleteConf(id):
    post = Post.query.get(id)
    return render_template('deleteConf.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

def dead_line_check(posts):
    for post in posts:
        date = post.post_date

        if date < datetime.now():
            db.session.delete(post)
            db.session.commit()
