from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utility.constants import UserRoles
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    password_changed = models.BooleanField(default=False)
    role = models.CharField(choices=[(e.value, e.value) for e in UserRoles], max_length=50)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        default_permissions = ('add', 'view', 'change', 'delete')
