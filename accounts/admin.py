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
            phone=user.phone, date_created=user.date_created,
            team="MA"
        )
    if user.team == "SA":
        SalesTeamEmployee.objects.create(
            id=user.id, email=user.email, password=user.password,
            first_name=user.first_name, last_name=user.last_name,
            phone=user.phone, date_created=user.date_created,
            team="SA"
        )
    if user.team == "SU":
        SupportTeamEmployee.objects.create(
            id=user.id, email=user.email, password=user.password,
            first_name=user.first_name, last_name=user.last_name,
            phone=user.phone, date_created=user.date_created,
            team="SU"
        )


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
            "fields": (
                "email", "team", "password1", "password2",
                "first_name", "last_name", "phone"
            ),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

    def has_module_permission(self, request):
        try:
            team = request.user.team
            if team == "WM":
                return True
        except:
            return False


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:
            create_user_in_corresponding_team_table(obj)

            for team, mod in zip(["MA", "SA", "SU"],
                                 [ManagerTeamEmployee, SalesTeamEmployee,
                                  SupportTeamEmployee]):
                try:
                    e_obj = mod.objects.get(id=obj.id)
                    if e_obj.team != team:
                        e_obj.delete(keep_parents=True)

                except:
                    pass


class ManagerTeamCreationForm(CommonCreationForm):

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        user.team = "MA"
        user.is_admin = determine_is_admin_status(user.team)
        return user


class ManagerTeamAdmin(UserAdmin):

    add_form = ManagerTeamCreationForm
    form = CommonChangeForm

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2",
                "first_name", "last_name", "phone"
            ),
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


class SalesTeamAdmin(UserAdmin):
    add_form = SalesTeamCreationForm
    form = CommonChangeForm

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2",
                       "first_name", "last_name", "phone"),
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


class SupportTeamAdmin(UserAdmin):
    add_form = SupportTeamCreationForm
    form = CommonChangeForm

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2",
                       "first_name", "last_name", "phone"),
        }),
    )

    def has_module_permission(self, request):
        return True


admin.site.register(Employee, UserAdmin)
admin.site.register(ManagerTeamEmployee, ManagerTeamAdmin)
admin.site.register(SalesTeamEmployee, SalesTeamAdmin)
admin.site.register(SupportTeamEmployee, SupportTeamAdmin)
admin.site.unregister(Group)
