from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


class EventPermissions(BasePermission):

    def has_permission(self, request, view):
        return True
        # print(f"\n\nuser:\n{request.user.team}\n")
        # if not request.user.is_authenticated:
        #     # return False
        #     raise NotAuthenticated(detail="Dois être login.")
        # return True


    def has_object_permission(self, request, view, obj):
        return False
        # user = request.user.team
        # if not request.user.is_authenticated or user == "SA":
        #     return False
        # # raise NotAuthenticated(detail="Dois être login.")
        # return True
