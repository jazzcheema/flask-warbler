"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py

import os
from unittest import TestCase

from models import db, User, Message, Follow
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

db.drop_all()
db.create_all()


class MessageModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        db.session.flush()

        m1 = Message(text="m1-text", user_id=u1.id)
        db.session.add_all([m1])
        db.session.commit()
        self.u1_id = u1.id
        self.m1_id = m1.id

    def tearDown(self):
        db.session.rollback()


    def test_message_model(self):
        u1 = User.query.get(self.u1_id)

        self.assertEqual(len(u1.messages), 1)

    def test_create_message(self):
        u1 = User.query.get(self.u1_id)
        m2 = Message(text="test_text", user_id=u1.id)
        db.session.add(m2)
        db.session.flush()


        self.assertIn('test_text', m2.text)



