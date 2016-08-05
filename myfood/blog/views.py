from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from ..models import Post, Permission, Comment, Category
from .forms import PostForm, CommentForm
from .. import db

mod = Blueprint('blog', __name__)


@mod.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    # check whether the category you want to add to the new post was already exist in the database,
    category = Category.query.filter_by(categoryname=form.category.data).first()
    if current_user.can(Permission.ADMINISTER) and form.validate_on_submit():
        # if the category is not exist in the database, create a new one whose data was got in the form
        if category is None:
            category = Category(categoryname=form.category.data)
            db.session.add(category)
        post = Post(body=form.body.data,
                    title=form.title.data,
                    category=category)
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/index.html', form=form, posts=posts)


@mod.route('/category/<int:id>')
def category(id):
    category = Category.query.get_or_404(id)
    posts = category.posts.order_by(Post.timestamp.desc()).all()
    return render_template('blog/category.html', posts=posts, category=category)


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
    comments = post.comments.order_by(Comment.timestamp.desc()).all()
    return render_template('blog/post.html', posts=[post], form=form, comments=comments)


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    category = Category.query.filter_by(categoryname=form.category.data).first()
    if form.validate_on_submit():
        if category is None:
            category = Category(categoryname=form.category.data)
            db.session.add(category)
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.filter_by(categoryname=form.category.data).first()
        db.session.add(post)
        flash('The post has been updated!')
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category.categoryname
    return render_template('blog/edit_post.html', form=form)


@mod.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    db.session.delete(post)
    flash('The post has been deleted.')
    return redirect(url_for('.index'))


@mod.route('/secret')
@login_required
def secret():
    return 'login required!'


@mod.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

