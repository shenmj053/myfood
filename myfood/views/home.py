from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Post, Permission, Comment
from ..forms import PostForm, CommentForm
from .. import db

mod = Blueprint('home', __name__)


@mod.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.ADMINISTER) and form.validate_on_submit():
        post = Post(body=form.body.data, title=form.title.data)
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('home/index.html', form=form, posts=posts)


@mod.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if current_user.can(Permission.COMMENT) and form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        return redirect(url_for('.post', id=post.id))
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template('home/post.html', posts=[post], form=form, comments=comments)


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if current_user.can(Permission.ADMINISTER) and form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('home/edit_post.html', form=form)


@mod.route('/secret')
@login_required
def secret():
    return 'login required!'


@mod.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

