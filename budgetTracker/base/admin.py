from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from .models import User, Category, Income, Expense, EMI, Budget, Alert, Report


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ["name", "email", "phone", "is_admin"]
    list_filter = ["is_admin"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal Info", {"fields": ["name", "phone"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "phone", "password1", "password2"],
            },
        ),
    ]

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)


# Unregister Group (optional, if not using built-in permissions)
admin.site.unregister(Group)

# Register other models
admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(EMI)
admin.site.register(Budget)
admin.site.register(Alert)
admin.site.register(Report)
