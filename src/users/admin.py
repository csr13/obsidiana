from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User
from admin_extend.admin import my_admin

class OxidianaAdminUser(UserAdmin):
    fieldsets = (
        (
            "INFO",
            {"fields" : ["email", "username", "password"]}
        ),
        (
            "PERMS",
            {"fields" : ["is_superuser", "is_staff"]}
        )
    )
    list_display = ["email", "username", "is_superuser", "is_staff"]

my_admin.register(User, OxidianaAdminUser)
