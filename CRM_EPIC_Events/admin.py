from django.contrib import admin


class WebMasterAdminSite(admin.AdminSite):

    def has_permission(self, request):
        if request.user.team == "WM":
            return True


class ManagerAdminSite(admin.AdminSite):

    def has_permission(self, request):
        if request.user.team == "MA":
            return True
