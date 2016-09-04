import time

from .base import FunctionalTest

TEST_EMAIL = 'edith@mockmyid.com'


class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # Edith goes to the superlists site
        # she notices a "Sign In" link
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        #   (use mockmyid.com) for test email
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys(TEST_EMAIL)
        self.wait_for(
            lambda: self.browser.find_element_by_tag_name('button').click(),
            timeout=50
        )

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # Edith can see that she is logged in
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Page refresh shows it is a real session
        #  not just a client-side one off for page
        self.browser.refresh()
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Edith clicks 'logout'
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(TEST_EMAIL)

        # logged-out status is persistent after refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(TEST_EMAIL)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')
