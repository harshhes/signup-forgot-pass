from django.contrib import admin
from .models import User

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['name', 'username', 'email', 'is_superuser', 'is_active']
    search_fields = ['email', 'username', 'name']