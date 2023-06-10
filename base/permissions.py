from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import BasePermission
from base.models import User

class UserPermission(BasePermission):
    ...

    