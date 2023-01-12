# from django.contrib import admin
#
# from .models import ManagerTeamEmployee
# from accounts.models import MyUser
#
#
# class AccountInline(admin.StackedInline):
#     model = MyUser
#     can_delete = True
#     extra = 0
#     fields = ("email", "password", "team", "is_admin")
#
#
# class ManagerInline(admin.StackedInline):
#     model = ManagerTeamEmployee
#     can_delete = True
#     extra = 0
#     fields = ("first_name", "last_name")
#
#
# class MemberAdmin(admin.ModelAdmin):
#     model = ManagerTeamEmployee
#     inlines = [AccountInline]
#     fieldsets = (
#         (None, {"fields": ("first_name", "last_name")}),
#     )