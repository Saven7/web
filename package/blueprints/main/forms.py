from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo
from package.core.models import User
from flask_babel import _, lazy_gettext as _l
from flask import request



class EditProfileForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	about_me = TextAreaField(_l('About me *'), validators=[Length(min=0, max=140)])
	email = StringField(_l('Email'), validators=[DataRequired(), Email()])
	password = PasswordField(_l('Password *'))
	password2 = PasswordField(
		_l('Repeat Password *'), validators=[EqualTo('password')])
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError(_('Please use a different username.'))



class EditProfileFormOther(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	about_me = TextAreaField(_l('About me *'), validators=[Length(min=0, max=140)])
	email = StringField(_l('Email'), validators=[DataRequired(), Email()])
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError(_('Please use a different username.'))



class PostForm(FlaskForm):
	post = TextAreaField(_l('Say something:'), validators=[
		DataRequired(), Length(min=1, max=140)])
	submit = SubmitField(_l('Submit'))



class GroupForm(FlaskForm):
	user_admin = BooleanField("set admin status; true/false")
	submit = SubmitField(_l('Submit'))



class SearchForm(FlaskForm):
	q = StringField(_l('Search'), validators=[DataRequired()])
	
	def __init__(self, *args, **kwargs):
		if 'formdata' not in kwargs:
			kwargs['formdata'] = request.args
		if 'csrf_enabled' not in kwargs:
			kwargs['csrf_enabled'] = False
		super(SearchForm, self).__init__(*args, **kwargs)