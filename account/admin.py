from django.contrib import admin
from account.models import User, Company
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["username", "password"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2"],
            },
        ),
    ]

    search_fields = ["username"]
    ordering = ["username"]
    filter_horizontal = []

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Company)