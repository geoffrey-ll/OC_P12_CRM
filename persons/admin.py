from django.contrib import admin

from persons.models import (
    Client, ManagerTeamEmployee, Prospect, SalesTeamEmployee,
    SupportTeamEmployee
)


class ManagerTeamEmployeeAdmin(admin.ModelAdmin):
    """Représentation des objets ManagerTeamEmployee dans l'administration
    Django.
    """
    # list_display = ("id", "account_email", "first_name", "last_name", "phone",
    #                 "date_created", "date_updated", "account_is_admin")
    # list_filter = ("is_admin",)
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    #     ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
    #     ("Permissions", {"fields": ("is_admin",)}),
    # )
    # search_fields = ("email",)
    # ordering = ("email",)
    # filter_horizontal = ()


class SalesTeamEmployeeAdmin(admin.ModelAdmin):
    """Représentation des objets SalesTeamEmployee dans l'administration
    Django.
    """
    # list_display = ("id", "account_email", "first_name", "last_name", "phone",
    #                 "date_created", "date_updated", "account_is_admin")


class SupportTeamEmployeeAdmin(admin.ModelAdmin):
    """Représentation des objets SupportTeamEmployee dans l'administration
    Django.
    """
    # list_display = ("id", "account_email", "first_name", "last_name", "phone",
    #                 "date_created", "date_updated", "account_is_admin")


class ClientAdmin(admin.ModelAdmin):
    """Représentation des objets Client dans l'administration Django."""
    # list_display = ("id", "first_name", "last_name", "phone",
    #                 "date_created", "date_updated",
    #                 "id_company", "id_sales_team_employee")


class ProspectAdmin(admin.ModelAdmin):
    """Représentation des objets Prospect dans l'administration Django."""
    # list_display = ("id", "first_name", "last_name", "phone",
    #                 "date_created", "date_updated",
    #                 "id_company", "id_last_contact", "date_last_contact")



admin.site.register(ManagerTeamEmployee, ManagerTeamEmployeeAdmin)
admin.site.register(SalesTeamEmployee, SalesTeamEmployeeAdmin)
admin.site.register(SupportTeamEmployee, SupportTeamEmployeeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Prospect, ProspectAdmin)
