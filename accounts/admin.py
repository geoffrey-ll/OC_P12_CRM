from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .managers import determine_is_admin_status
from .models import (
    Employee, SalesTeamEmployee, SupportTeamEmployee, ManagerTeamEmployee)


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


class CommonCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def save(self, commit=True, *args, **kwargs):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print(f"\n\nTestCreation\n{user.team}\n")
        user.is_admin = determine_is_admin_status(user.team)
        if commit:
            user.save()
        # create_user_in_corresponding_team_table(user)
        return user


class CommonChangeForm(UserChangeForm):
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
    form = CommonChangeForm
    add_form = CommonCreationForm

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

    def has_module_permission(self, request):
        user = request.user
        if user.team == "WM":
            return True
        if user.team == "MA":
            return False



class ManagerTeamCreationForm(CommonCreationForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        user.team = "MA"
        user.is_admin = determine_is_admin_status(user.team)
        return user


class ManagerTeamChangeForm(CommonChangeForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        ManagerTeamEmployee.objects.filter(id=user.id).delete(keep_parents=True)
        create_user_in_corresponding_team_table(user)
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

    def has_module_permission(self, request):
        return True


class SalesTeamCreationForm(CommonCreationForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        user.team = "SA"
        user.is_admin = determine_is_admin_status(user.team)
        return user


class SalesTeamChangeForm(CommonChangeForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        TEST02 = SalesTeamEmployee.objects.filter(id=user.id)
        TEST02.delete()
        create_user_in_corresponding_team_table(user)
        return user


class SalesTeamAdmin(UserAdmin):
    add_form = SalesTeamCreationForm
    form = SalesTeamChangeForm

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "phone"),
        }),
    )

    def has_module_permission(self, request):
        return True


class SupportTeamCreationForm(CommonCreationForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        user.team = "SU"
        user.is_admin = determine_is_admin_status(user.team)
        return user


class SupportTeamChangeForm(CommonChangeForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        TEST02 = SupportTeamEmployee.objects.filter(id=user.id)
        TEST02.delete()
        create_user_in_corresponding_team_table(user)
        return user


class SupportTeamAdmin(UserAdmin):
    add_form = SupportTeamCreationForm
    form = SupportTeamChangeForm

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "phone"),
        }),
    )

    def has_module_permission(self, request):
        return True


admin.site.register(Employee, UserAdmin)
admin.site.register(ManagerTeamEmployee, ManagerTeamAdmin)
admin.site.register(SalesTeamEmployee, SalesTeamAdmin)
admin.site.register(SupportTeamEmployee, SupportTeamAdmin)
admin.site.unregister(Group)
