"""User View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# This is a bit of hack, but don't use Flask DebugToolbar

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_log_in(self):
        with app.test_client() as c:

            resp = c.get("/login")
            html = resp.get_data(as_text=True)

            self.assertIn('Welcome back.', html)
            self.assertEqual(resp.status_code, 200)

    def test_log_in_session(self):
        with app.test_client() as c:

            resp = c.post("/login", data={"username": "u1",
                                          "password": "password"},
                                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('<!-- home_page_for_users -->', html)
            self.assertEqual(resp.status_code, 200)

    def test_log_out(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.post("/logout", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("What's Happening?", html)
            self.assertEqual(resp.status_code, 200)










