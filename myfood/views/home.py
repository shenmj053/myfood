from flask import Blueprint, render_template, redirect, url_for
from ..models import Post
from ..forms import PostForm
from .. import db

mod = Blueprint('home', __name__)


@mod.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, title=form.title.data)
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('home/index.html', form=form, posts=posts)


@mod.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('home/post.html', posts=[post])


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('home/edit_post.html', form=form)



