from flask import render_template, flash, redirect, url_for, request, g, current_app, g
from package.core import db
from .forms import EditProfileForm, PostForm, GroupForm, SearchForm
from flask_login import current_user, login_user, logout_user, login_required
from package.core.models import User, Post
from datetime import datetime
from flask_babel import _, get_locale
from . import bp



@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
		g.search_form = SearchForm()
	g.locale = str(get_locale())



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(_('Your post is now online!'))
		return redirect(url_for('main.index'))
	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title=_('Home Page'), form=form, posts=posts.items,
		next_url=next_url, prev_url=prev_url)



@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.explore', username=user.username, page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('main.explore', username=user.username, page=posts.prev_num) \
		if posts.has_prev else None
	form = GroupForm()
	if form.validate_on_submit():
		user.user_admin = form.user_admin.data
		db.session.commit()
		db.session.commit()
		flash(_('%(user1)s is admin: %(boolu)s', user1=user.username, boolu=form.user_admin.data))
		return redirect(url_for('main.user', username=user.username))
	return render_template('user.html', user=user, form=form, posts=posts.items,
		next_url=next_url, prev_url=prev_url, app=current_app)



@bp.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	user = current_user
	if form.validate_on_submit():
		user.username = form.username.data
		user.about_me = form.about_me.data
		user.email = form.email.data
		if len(form.password.data) > 0:
			user.set_password(form.password.data)
		db.session.commit()
		flash(_('Your changes have been saved.'))
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = user.username
		form.email.data = user.email
		form.about_me.data = user.about_me
	return render_template('edit_profile.html', title='Edit Profile', user=user, form=form)



@bp.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile_other(username):
	if not current_user.is_admin():
		return redirect(url_for('main.edit_profile'))
	form = EditProfileForm(username)
	user = User.query.filter_by(username=username).first_or_404()
	if form.validate_on_submit():
		user.username = form.username.data
		user.about_me = form.about_me.data
		user.email = form.email.data
		db.session.commit()
		flash(_('Your changes have been saved.'))
		return redirect(url_for('main.user', username=user.username))
	elif request.method == 'GET':
		form.username.data = user.username
		form.email.data = user.email
		form.about_me.data = user.about_me
	return render_template('edit_profile.html', title='Edit Profile', user=user, form=form)



@bp.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user is None:
		flash(_('User %(user1)s not found.', user1=username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('main.user', username=user))
	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(user1)s now!', user1=username))
	return redirect(url_for('main.user', username=username))



@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user is None:
		flash(_('User %(user1)s not found.', user1=username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash(_('You cannot unfollow yourself!'))
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash(_('You are no longer following %(user1)s!', user1=username))
	return redirect(url_for('main.user', username=username))



@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	return render_template('index.html', title='Explore', posts=posts.items)



@bp.route('/search')
@login_required
def search():
	if not g.search_form.validate():
		return redirect(url_for('.explore'))
	page = request.args.get('page', 1, type=int)
	posts, total = Post.search(g.search_form.q.data, page,
		current_app.config['POSTS_PER_PAGE'])
	next_url = url_for('.search', q=g.search_form.q.data, page=page + 1) \
		if total > page * current_app.config['POSTS_PER_PAGE'] else None
	prev_url = url_for('.search', q=g.search_form.q.data, page=page - 1) \
		if total > 1 else None
	return render_template('search.html', title=_('Search'), posts=posts,
		next_url=next_url, prev_url=prev_url)
