from django.contrib.auth import get_user_model
import requests

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'
User =  get_user_model()

class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': DOMAIN}
        )
        if response.ok and response.json()['status'] == 'okay':
            return User.objects.get(email=response.json()['email'])
