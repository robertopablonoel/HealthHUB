import unittest
from flask import render_template, redirect, request, url_for, flash
from app import create_app, db
from app.models import User, Role
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.home'))
        #Since not logged in should return false
        self.assertFalse('Newsletter' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # register a new account
        response = self.client.post(url_for('auth.register_patient'), data={
            'email': 'demo@demo.com', 'first_name': 'john','last_name' : 'fruscante', 'password': 'cataclismic', 'password2': 'cataclismic',
             'date_of_birth' : '01/01/2997'
        })
        self.assertTrue(response.status_code == 302)
                # login with the new account
        response = self.client.post(url_for('auth.login'), data={ 'email': 'demo@demo.com',
        'password': 'cataclismic'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have not confirmed your account yet' in data)
        user = User.query.filter_by(email='demo@demo.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)
