"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follow
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)


    def test_user_model_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)

        self.assertEqual(u1.is_following(u2), True)

    def test_user_model_not_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertEqual(u1.is_following(u2), False)

    def test_user_model_followed_by(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)


        u2.following.append(u1)

        self.assertTrue(u1.is_followed_by(u2))

    def test_user_model_followed_by_other_user(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_followed_by(u2))

    def test_user_signup_on_valid(self):
        u3 = User.signup("u3", "u3@email.com", "password", None)
        db.session.flush()

        test_found_user = User.query.filter_by(username = 'u3').first()

        self.assertTrue(u3 == test_found_user)

    def test_user_signup_invalid(self):
        try:
            User.signup("u3", "u3@email.com", "password", None)
            db.session.flush()
            User.signup("u4", "u3@email.com", "password", None)
            db.session.flush()
        except IntegrityError as error:
            self.assertIn("unique constraint", str(error))

    def test_user_authenticate(self):
        u1 = User.query.get(self.u1_id)
        test_user = User.authenticate(u1.username, 'password')
        self.assertTrue(test_user == u1)

    def test_user_username_fail_authenticate(self):
        u1 = User.query.get(self.u1_id)
        test_user = User.authenticate('failed', 'password')
        self.assertFalse(test_user == u1)

    def test_user_password_fail_authenticate(self):
        u1 = User.query.get(self.u1_id)
        test_user = User.authenticate(u1.username, u1.password)
        self.assertFalse(test_user == u1)









