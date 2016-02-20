from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys

class FunctionalTest(StaticLiveServerTestCase):
    """
    Base class for other functional tests.
    """
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        # profile = webdriver.FirefoxProfile()
        # profile.set_preference("browser.startup.homepage", "about:blank");
        # profile.set_preference("startup.homepage_welcome_url", "about:blank");
        # profile.set_preference("startup.homepage_welcome_url.additional", "about:blank");
        # self.browser = webdriver.Firefox(profile)

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        #self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        box = self.browser.find_element_by_id('id_text')
        return box
