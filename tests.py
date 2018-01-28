#!/usr/bin/env python
from package.core import create_app, db
from package.core.models import User, Post
from datetime import datetime, timedelta
from config import Config
import unittest



class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite://'



class UserModelCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
	
	
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
	
	
	def test_password_hashing(self):
		u = User(username='test')
		u.set_password('check')
		self.assertFalse(u.check_password('test'))
		self.assertTrue(u.check_password('check'))
	
	
	def test_avatar(self):
		u = User(username='check', email='no-reply@mavki.com')
		self.assertEqual(u.avatar(128), ('http://www.gravatar.com/avatar/'
										'7f460bb7dac63b8548cceb1cee8d4f01'
										'?d=identicon&s=128'))
	
	
	def test_follow(self):
		u1 = User(username='check', email='check@test.com')
		u2 = User(username='test', email='test@check.com')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertEqual(u1.followed.all(), [])
		self.assertEqual(u1.followers.all(), [])

		u1.follow(u2)
		db.session.commit()
		self.assertTrue(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 1)
		self.assertEqual(u1.followed.first().username, 'test')
		self.assertEqual(u2.followers.count(), 1)
		self.assertEqual(u2.followers.first().username, 'check')

		u1.unfollow(u2)
		db.session.commit()
		self.assertFalse(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 0)
		self.assertEqual(u2.followers.count(), 0)

	def test_follow_posts(self):
		u1 = User(username='s1', email='s1@ct.com')
		u2 = User(username='s2', email='s2@ct.com')
		u3 = User(username='s3', email='s3@ct.com')
		u4 = User(username='s4', email='s4@ct.com')
		db.session.add_all([u1, u2, u3, u4])

		now = datetime.utcnow()
		p1 = Post(body='post by s1', author=u1,
			 timestamp=now + timedelta(seconds=1))
		p2 = Post(body='post by s2', author=u2,
			 timestamp=now + timedelta(seconds=1))
		p3 = Post(body='post by s3', author=u3,
			 timestamp=now + timedelta(seconds=1))
		p4 = Post(body='post by s4', author=u4,
			 timestamp=now + timedelta(seconds=1))
		db.session.add_all([p1, p2, p3, p4])
		db.session.commit()

		u1.follow(u2)
		u1.follow(u4)
		u2.follow(u3)
		u3.follow(u4)
		db.session.commit()
		f1 = u1.followed_posts().all()
		f2 = u2.followed_posts().all()
		f3 = u3.followed_posts().all()
		f4 = u4.followed_posts().all()
		self.assertEqual(f1, [p1, p2, p4])
		self.assertEqual(f2, [p2, p3])
		self.assertEqual(f3, [p3, p4])
		self.assertEqual(f4, [p4])

if __name__ == '__main__':
	unittest.main(verbosity=2)