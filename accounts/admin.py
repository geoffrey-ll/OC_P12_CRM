from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import BaseModelForm

from .models import Employee, SalesTeamEmployee, SupportTeamEmployee, ManagerTeamEmployee
from .managers import determine_is_admin_status


def create_user_in_corresponding_team_table(user):
    if user.team == "MA":
        ManagerTeamEmployee.objects.create(
            id=user.id, email=user.email, password=user.password,
            first_name=user.first_name, last_name=user.last_name,
            phone=user.phone, date_created=user.date_created)
    if user.team == "SA":
        SalesTeamEmployee.objects.create(
            id=user.id, email=user.email, password=user.password,
            first_name=user.first_name, last_name=user.last_name,
            phone=user.phone, date_created=user.date_created)
    if user.team == "SU":
        SupportTeamEmployee.objects.create(
            id=user.id, email=user.email, password=user.password,
            first_name=user.first_name, last_name=user.last_name,
            phone=user.phone, date_created=user.date_created)


class TestCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def save(self, commit=True, *args, **kwargs):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_admin = determine_is_admin_status(user.team)
        user.save()
        create_user_in_corresponding_team_table(user)
        return user


class TestChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = determine_is_admin_status(user.team)
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = TestChangeForm
    add_form = TestCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("id", "email", "team",
                    "first_name", "last_name", "phone",
                    "is_admin", "is_staff")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Add info", {"fields": ("team", "first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("is_admin", "is_staff")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "team", "password1", "password2", "first_name", "last_name", "phone"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()




class ManagerTeamCreationForm(TestCreationForm):

    def save(self, commit=True, *args, **kwargs):
        print(f"\n\nPasse dans ManagerCreationForm.save\n")
        user = super().save(commit=False)
        user.team = "MA"
        return user


class ManagerTeamChangeForm(TestChangeForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        TEST02 = ManagerTeamEmployee.objects.filter(id=user.id)
        TEST02.delete()
        create_user_in_corresponding_team_table(user)
        TEST01 = ManagerTeamEmployee.objects.all()
        print(f"\n\nuser{user}\n")
        print(f"\n\nuser.id\n{user.id}\n")
        print(f"\n\nTEST01\n{TEST01}\n")
        print(f"\n\nTEST02\n{TEST02}\n")
        return user


class ManagerTeamAdmin(UserAdmin):
    add_form = ManagerTeamCreationForm
    form = ManagerTeamChangeForm

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "phone"),
        }),
    )


# Now register the new UserAdmin...
admin.site.register(Employee, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.register(ManagerTeamEmployee, ManagerTeamAdmin)
admin.site.register(SalesTeamEmployee, UserAdmin)
admin.site.register(SupportTeamEmployee, UserAdmin)
admin.site.unregister(Group)
