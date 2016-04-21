from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch

from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)
User = get_user_model()

@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()

    def test_sends_assertion_to_mozilla_with_doimain(self, mock_post):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': DOMAIN}
        )

    def test_returns_None_if_response_errors(self, mock_post):
        mock_post.return_value.ok = False
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_returns_None_if_status_not_ok(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {
            'status': 'okay', 'email': 'a@b.com'
        }
        actual_user = User.objects.create(email='a@b.com')
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(found_user, actual_user)
