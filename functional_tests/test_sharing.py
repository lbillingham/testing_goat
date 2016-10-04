from selenium import webdriver
from .base import FunctionalTest
fro .home_and_list_pages import HomePage


def quit_if_possible(browser):
    try: browser.quit()
    except: pass


class SharingTest(FunctionalTest):

    def test_logged_in_users_tests_are_saved_as_my_list(self):
        # Edith is a logged in user
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Her friend Bob also logs in on the lists site
        bob_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(bob_browser))
        self.browser = bob_browser
        self.create_pre_authenticated_session('bob@example.com')

        # Edith goes to her home page and starts a list
        self.browser = edith_browser
        list_page = HomePage(self).start_new_list('Get help')

        # Edith notices a 'Share this list' option

        # She notices a "Share this list" option
        # self.wait_for(
        #     lambda:  self.assertEqual(
        #     self.browser.find_element_by_css_selector(
        #         'input[name=email]'
        #     ).get_attribute('placeholder'),
        #     'your-friend@example.com'
        #     )
        # )
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # Edith shares her list
        # and sees that it updates to show it is shared with Bob
        list_page.share_list_with('bob@example.com')
