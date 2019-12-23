import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Firefox
        try:
            cls.client = webdriver.Chrome()
        except:
            pass
        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            admin_role = Role.query.filter_by(permissions=0x80).first()
            admin = User(email='demo@demo.com',
                        first_name = "demoman",
                        last_name = "demoman",
                         password='cataclismic1',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()
            threading.Thread(target=cls.app.run).start()
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()
            db.drop_all()
            db.session.remove()
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Login', self.client.page_source))

        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cataclismic1')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Newsletter', self.client.page_source))

    def test_forum(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Login', self.client.page_source))

        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cataclismic1')
        self.assertTrue(re.search('Newsletter', self.client.page_source))
        #Getting the forum and asseting arrival
        self.client.find_element_by_name('forum').click()
        self.assertTrue(re.search('Top Forums', self.client.page_source))

    def test_forum_posts(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Login', self.client.page_source))

        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cataclismic1')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Newsletter', self.client.page_source))
        #Getting the forum and asseting arrival
        self.client.find_element_by_name('forum').click()
        self.assertTrue(re.search('Top Forums', self.client.page_source))

        self.client.find_element_by_name("b1_forum").click()
        self.assertTrue(re.search('Post', self.client.page_source))

        #Checking if the posts submit and appear on screen
        self.client.find_element_by_name("post-input").send_keys('Demo Forum Info for Test Purposes')
        self.client.find_element_by_name("post-button").click()
        self.assertTrue(re.search('Demo Forum Info for Test Purposes', self.client.page_source))

    def test_scheduling(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Login', self.client.page_source))

        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cataclismic1')
        self.client.find_element_by_name('submit').click()

        self.assertTrue(re.search('Newsletter', self.client.page_source))

        self.client.find_element_by_name('book-appointment').click()
        self.assertTrue(re.search('Calendar', self.client.page_source))

        self.client.find_element_by_name('reason').send_keys("I'm not feeling well temp")
        self.client.find_element_by_name('book').click()
        self.assertTrue(re.search('Successfully Booked', self.client.page_source))

    def test_user_profile(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Login', self.client.page_source))

        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cataclismic1')
        self.client.find_element_by_name('submit').click()

        self.assertTrue(re.search('Newsletter', self.client.page_source))
        self.client.find_element_by_name('user-profile').click()

        self.assertTrue(re.search('First Name:', self.client.page_source))


    def test_user_search(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Login', self.client.page_source))

        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cataclismic1')
        self.client.find_element_by_name('submit').click()

        self.assertTrue(re.search('Newsletter', self.client.page_source))
        self.client.find_element_by_name('user-search').click()

        self.assertTrue(re.search('Search', self.client.page_source))
        self.client.find_element_by_name('search-input').send_keys("demoman")

        self.client.find_element_by_name('search-submit').click()
        self.assertTrue(re.search('demoman', self.client.page_source))

    def test_user_prescriptions(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Login', self.client.page_source))

        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cataclismic1')
        self.client.find_element_by_name('submit').click()

        self.assertTrue(re.search('Newsletter', self.client.page_source))
        self.client.find_element_by_name('user-search').click()

        self.assertTrue(re.search('Search', self.client.page_source))
        self.client.find_element_by_name('search-input').send_keys("demoman")

        self.client.find_element_by_name('search-submit').click()
        self.assertTrue(re.search('demoman', self.client.page_source))

        self.client.find_element_by_name('new-prescription').click()
        self.assertTrue(re.search('Days', self.client.page_source))
