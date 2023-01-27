from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm

from persons.models import (
    Client, Prospect, Person
)

from accounts.models import ManagerTeamEmployee, SalesTeamEmployee, SupportTeamEmployee


class ClientAdmin(admin.ModelAdmin):
    """Représentation des objets Client dans l'administration Django."""
    list_display = ("id", "sales_employee",
                    "first_name", "last_name", "phone",
                    "date_created", "date_updated",
                    "company")


class ProspectAdmin(admin.ModelAdmin):
    """Représentation des objets Prospect dans l'administration Django."""
    list_display = ("id", "last_sales_contacted", "date_last_contact",
                    "first_name", "last_name", "phone",
                    "date_created", "date_updated",
                    "company")



admin.site.register(Client, ClientAdmin)
admin.site.register(Prospect, ProspectAdmin)
# admin.site.register(Person)
