from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models


class ListUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == 'laurence@example.com'

    @property
    def is_active(self):
        return True


class ListUserManager(BaseUserManager):

    def create_user(self, eamil):
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email)