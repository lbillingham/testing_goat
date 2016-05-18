from django.conf import settings

from .base import FunctionalTest
from .server_tools import create_session_on_server
from management.commands.create_session import create_pre_authenticated_session


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
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'

        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # make Edith logged in
        self.create_pre_authenticated_session(email)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
