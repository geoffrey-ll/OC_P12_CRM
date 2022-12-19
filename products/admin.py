from django.contrib import admin

from .models import (Contract, Event)


class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "id_client", "contract_number", "payment_due", 
                    "closed")


class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "id_employee_support", "id_contract", "id_location",
                    "status", "start_event", "end_event", "attendees", "notes")
    pass


admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)