from django.contrib import admin

from .models import Company, Location


def concatenate_all_elmt_of_address(obj):
    """Concaténe tous les éléments de l'adresse."""
    return f"{obj.street_number}\n" \
           f"{obj.bis_ter}\n" \
           f"{obj.street_name}\n" \
           f"{obj.zip_code}\n" \
           f"{obj.town_name}\n" \
           f"{obj.country}"


class CompanyAdmin(admin.ModelAdmin):
    """Représentation des objets Company dans l'administration Django."""
    list_display = ("id", "siren", "name", "designation", "date_created", "date_updated")


class LocationAdmin(admin.ModelAdmin):
    """Représentation des objets Location dans l'administration Django."""
    list_display = ("id", "nic", "designation", "full_address")

    @staticmethod
    def full_address(obj):
        """Renvoi l'adresse complète."""
        return concatenate_all_elmt_of_address(obj)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Location, LocationAdmin)
