import os
import uuid
import base64
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from . import db
from .models import User, Post, Comment
from .forms import RegistrationForm, LoginForm, PostForm, CommentForm, EditProfileForm, SearchForm

main = Blueprint('main', __name__)

def save_image(form_image, folder='post_images'):
    """Handle image upload for Vercel - return default for now"""
    try:
        if form_image and form_image.filename:
            # For Vercel deployment, just return default image
            # In production, upload to cloud storage (AWS S3, Cloudinary, etc.)
            return 'default.jpg'
        return 'default.jpg'
    except Exception as e:
        print(f"Image save error: {e}")
        return 'default.jpg'

@main.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    tab = request.args.get('tab', 'for_you')
    posts = []
    if current_user.is_authenticated:
        if tab == 'featured':
            posts = current_user.followed_posts().all()
        else:
            # For you: could be AI-powered, but let's just show all + recommended for now
            posts = Post.query.order_by(Post.date_posted.desc()).all()
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts, search_form=search_form, tab=tab)

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    query = request.args.get('query', None) or (form.query.data if form.validate_on_submit() else None)
    results = []
    if query:
        results = Post.query.filter(Post.title.ilike(f"%{query}%")).all()
    return render_template('search_results.html', form=form, query=query, results=results)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login failed. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = save_image(form.image.data)
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image_file=filename,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', form=form)

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            content=form.content.data,
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added.', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    is_following = current_user.is_authenticated and current_user.is_following(post.author)
    is_saved = current_user.is_authenticated and current_user.has_saved_post(post)
    return render_template('post.html', post=post, form=form, is_following=is_following, is_saved=is_saved)

# New Route: Edit Post
@main.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.image.data:
            post.image_file = save_image(form.image.data)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')

# New Route: Delete Post
@main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))

@main.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        abort(403)
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {user.username}', 'success')
    return redirect(request.referrer or url_for('main.index'))

@main.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        abort(403)
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You unfollowed {user.username}', 'success')
    return redirect(request.referrer or url_for('main.index'))

@main.route('/save_post/<int:post_id>', methods=['POST'])
@login_required
def save_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user.save_post(post)
    db.session.commit()
    flash('Post saved!', 'success')
    return redirect(request.referrer or url_for('main.index'))

@main.route('/unsave_post/<int:post_id>', methods=['POST'])
@login_required
def unsave_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user.unsave_post(post)
    db.session.commit()
    flash('Post unsaved!', 'info')
    return redirect(request.referrer or url_for('main.index'))

@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    is_my_profile = current_user.is_authenticated and user.id == current_user.id
    is_following = current_user.is_authenticated and current_user.is_following(user)
    return render_template('profile.html', user=user, posts=posts, is_my_profile=is_my_profile, is_following=is_following)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        if form.profile_image.data:
            filename = save_image(form.profile_image.data, folder='profile_images')
            current_user.profile_image = filename
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('main.profile', username=current_user.username))
    return render_template('edit_profile.html', form=form)

@main.route('/saved')
@login_required
def saved():
    posts = current_user.saved.order_by(Post.date_posted.desc()).all()
    return render_template('saved.html', posts=posts)