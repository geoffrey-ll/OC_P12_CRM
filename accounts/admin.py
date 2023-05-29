"""Admin des comptes.

Permet la configuration des différentes tables d'utilisateurs (parent et
enfants), de leurs sauvegardes et leurs modifications.
"""
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .errors_messages import mess_errors_change_teams
from .models import (
    Employee, ManagerTeamEmployee, SalesTeamEmployee, SupportTeamEmployee)
from CRM_EPIC_Events.settings import EMPLOYEE_TEAM


def create_user_in_corresponding_team_table(user):
    """Créer l'user dans sa table respective."""
    for team_zip, model_zip in zip(
            EMPLOYEE_TEAM,
            [ManagerTeamEmployee, SalesTeamEmployee, SupportTeamEmployee]):
        if team_zip == user.team:
            model_zip.objects.create(
                id=user.id, email=user.email, password=user.password,
                first_name=user.first_name, last_name=user.last_name,
                phone=user.phone, date_created=user.date_created,
                team=team_zip)
            return


class CommonCreationForm(UserCreationForm):
    """Part commune des CreationForm des 4 teams."""

    def save(self, commit=True, *args, **kwargs):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CommonChangeForm(UserChangeForm):
    """Part commune des ChangeForm des 4 teams."""

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    """Part commune d'Admin pour les 4 teams.

    Sert aussi d'Admin à Webmaster (WM) car c'est la team de plus haut
    niveau.
    Un compte WM peut voir les comptes WM dans l'Admin. Ce qui n'est pas
    le cas des comptes manager (MA).
    """

    form = CommonChangeForm
    add_form = CommonCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("id", "email", "team",
                    "first_name", "last_name", "phone",)
    list_filter = ("team",)
    fieldsets = (
        ("Identifiant", {"fields": ("email", "password")}),
        ("Permission", {"fields": ("team",)}),
        ("Autres informations", {
            "fields": ("first_name", "last_name", "phone")
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ("Identifiant", {"fields": ("email", "password1", "password2")}),
        ("Permission", {"fields": ("team",)}),
        ("Autres informations", {
            "fields": ("first_name", "last_name", "phone")
        }),
    )

    search_fields = ("email",)
    search_help_text = "Recherche (partielle) dans les email"
    ordering = ("email",)
    filter_horizontal = ()

    def has_module_permission(self, request):
        """Gere la visibilité des comptes Webmaster.

        Las comptes Webmaster sont uniquement visible par les comptes
        Webmaster.
        """
        try:
            team = request.user.team
            if team == "WM":
                return True
        except:
            return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            for team_zip, model_zip in zip(
                    EMPLOYEE_TEAM, [ManagerTeamEmployee, SalesTeamEmployee,
                                    SupportTeamEmployee]):
                try:
                    model_zip.objects.get(id=obj.id)
                    if obj.team != team_zip:
                        try:
                            # Si obj.delete échoue, c'est parce que obj
                            # est rattaché à d'autres instances par
                            # ForeignKey, avec des
                            # on_delete=models.RESTRICT.
                            obj.delete(keep_parents=True)
                            create_user_in_corresponding_team_table(obj)
                        except:
                            # Si obj.delete a échoué, on remet à l'user
                            # son ancienne team et on envoie un message
                            # pour prévenir.
                            obj.team = team_zip
                            obj.save()
                            for team_err_zip, message_zip in zip(
                                    EMPLOYEE_TEAM, mess_errors_change_teams):
                                if team_zip == team_err_zip:
                                    messages.add_message(
                                        request, messages.ERROR, message_zip)
                        return
                except:
                    continue


class ManagerTeamCreationForm(CommonCreationForm):
    """CreationForm spécifique à la team Manager."""

    def save(self, commit=True, *args, **kwargs):
        """Surcharge du save de CommonCreationForm."""
        user = super().save(commit=False)
        user.team = "MA"
        return user


class ManagerTeamAdmin(UserAdmin):
    """Admin spécifique à la table Manager."""

    add_form = ManagerTeamCreationForm
    form = CommonChangeForm
    add_fieldsets = (
        ("Identifiant", {"fields": ("email", "password1", "password2")}),
        ("Autres informations", {
            "fields": ("first_name", "last_name", "phone")
        }),
    )

    def has_module_permission(self, request):
        return True


class SalesTeamCreationForm(CommonCreationForm):
    """CreationForm spécifique à la team Sales."""

    def save(self, commit=True, *args, **kwargs):
        """Surcharge du save de CommonCreationForm."""
        user = super().save(commit=False)
        user.team = "SA"
        return user


class SalesTeamAdmin(UserAdmin):
    """Admin spécifique à la table Sales."""
    add_form = SalesTeamCreationForm
    form = CommonChangeForm
    add_fieldsets = (
        ("Identifiant", {"fields": ("email", "password1", "password2")}),
        ("Autres informations", {
            "fields": ("first_name", "last_name", "phone")
        }),
    )

    def has_module_permission(self, request):
        return True


class SupportTeamCreationForm(CommonCreationForm):
    """CreationForm spécifique à la team Support."""

    def save(self, commit=True, *args, **kwargs):
        """Surcharge du save de CommonCreationForm."""
        user = super().save(commit=False)
        user.team = "SU"
        return user


class SupportTeamAdmin(UserAdmin):
    """Admin spécifique à la table Support."""

    add_form = SupportTeamCreationForm
    form = CommonChangeForm
    add_fieldsets = (
        ("Identifiant", {"fields": ("email", "password1", "password2")}),
        ("Autres informations", {
            "fields": ("first_name", "last_name", "phone")
        }),
    )

    def has_module_permission(self, request):
        return True


admin.site.register(Employee, UserAdmin)
admin.site.register(ManagerTeamEmployee, ManagerTeamAdmin)
admin.site.register(SalesTeamEmployee, SalesTeamAdmin)
admin.site.register(SupportTeamEmployee, SupportTeamAdmin)
admin.site.unregister(Group)
