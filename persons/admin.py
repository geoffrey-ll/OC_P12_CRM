"""Admin de l'app persons."""
from django.contrib import admin

from .models import Client, Prospect


class ClientAdmin(admin.ModelAdmin):

    list_display = ("id", "sales_employee",
                    "first_name", "last_name", "phone", "email",
                    "date_created", "date_updated",
                    "company")


class ProspectAdmin(admin.ModelAdmin):

    list_display = ("id", "sales_employee",
                    "first_name", "last_name", "phone", "email",
                    "date_last_contact", "company",
                    "date_created", "date_updated",)


admin.site.register(Client, ClientAdmin)
admin.site.register(Prospect, ProspectAdmin)
