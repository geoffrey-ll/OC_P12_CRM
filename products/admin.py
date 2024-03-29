"""Admin de l'app products."""
from django.contrib import admin

from .models import Contract, Event


class ContractAdmin(admin.ModelAdmin):

    list_display = ("id", "client", "contract_number",
                    "amount", "payment_due", "closed",
                    "date_created", "date_updated")


class EventAdmin(admin.ModelAdmin):

    list_display = ("id", "support_employee", "contract", "location",
                    "status", "start_event", "end_event", "attendees",
                    "notes")


admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
