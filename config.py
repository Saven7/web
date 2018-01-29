import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dir = os.path.join(basedir, 'package/data')
load_dotenv(os.path.join(dir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(dir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	POSTS_PER_PAGE = 14
	ADMINS = os.environ.get('ADMINS')
	HIRE = os.environ.get('HIRE')
	LANGUAGES = ['en', 'de', 'fr', 'hu', 'es']
	LANGUAGES_OTHER = ['ja', 'ru', 'zh', 'la']
	ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
