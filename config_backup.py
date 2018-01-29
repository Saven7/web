import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dir = os.path.join(basedir, 'package\data')
load_dotenv(os.path.join(dir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or '[;f&t//i3Y)!E_8'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'package/data/app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'mavki.bot'
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Sein576!'
	POSTS_PER_PAGE = 14
	ADMINS = os.environ.get('ADMINS') or ['maske.soeren@gmail.com']
	HIRE = os.environ.get('HIRE')
	LANGUAGES = ['en', 'de', 'fr', 'hu', 'es']
	LANGUAGES_OTHER = ['ja', 'ru', 'zh', 'la']
	ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
