import time

from django.conf import settings

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## want to set cookie, hence visit domain
        ## 404 pages load fast
        self.browser.get(self.server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')

        # Edith goes to the home page and starts a list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('reticulate splines\n')
        self.get_item_input_box().send_keys('Immanentize eschaton\n')
        first_list_url = self.browser.current_url

        # she notices a 'My lists link, for the 1st time'
        self.browser.find_element_by_link_text('My lists').click()

        # She sees that her list is in there, named according to
        #  its first list item
        self.browser.find_element_by_link_text('reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url),
            timeout=150
        )

        # she decides to start another list, just to be sure
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Click cows\n')
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url),
            timeout=50
        )

        # she logs out. The "My Lists" option dissapears
        self.browser.find_element_by_id('id_logout').click()
        self.wait_for(
            self.assertEqual(
                lambda: self.browser.find_elements_by_link_text('My lists'),
                []
            ),
            timeout=50
        )
        # email = 'edith@example.com'
        #
        # self.browser.get(self.server_url)
        # self.wait_to_be_logged_out(email)
        #
        # # make Edith logged in
        # self.create_pre_authenticated_session(email)
        #
        # self.browser.get(self.server_url)
        # self.wait_to_be_logged_in(email)
