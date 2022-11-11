from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person


# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(Person, PersonAdmin)
