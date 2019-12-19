import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u1 = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        u2 = User(email = "default1@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        self.assertTrue(u1.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        u2 = User(email = "default1@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_roles_and_permissions(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        self.assertTrue(u.can(Permission.PATIENT_PERMISSION))
        self.assertFalse(u.can(Permission.PHYSICIAN_PERMISSION))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.PATIENT_PERMISSION))

    def test_timestamps(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User(email = "default@demo.com", password='cat', first_name = "test_user", last_name = "test_user")
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)
