from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

from CRM_EPIC_Events.commons_functions import get_locations_of_clients_and_events
from CRM_EPIC_Events.settings import ADMIN_TEAM
from additional_data.models import Company, Location
from persons.models import Client
from products.models import Contract, Event


class ContractPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.team == "SU":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team in ADMIN_TEAM:
            return True
        else:
            pk_contract = view.kwargs.get("pk")
            contract = Contract.objects.get(id=pk_contract)
            if user.team == "SA" and contract.client.sales_employee.id == user.id:
                return True
            else:
                return request.method in SAFE_METHODS


class EventPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not view.detail and user.team == "SU":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team in ADMIN_TEAM:
            return True
        else:
            pk_event = view.kwargs.get("pk")
            event = Event.objects.get(id=pk_event)
            if user.team == "SU" and event.support_employee.id == user.id:
                return True
            else:
                return request.method in SAFE_METHODS


class PersonPermission(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class CompanyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.team == "SU":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team in ADMIN_TEAM:
            return True
        else:
            if user.team == "SA":
                clients_handle = Client.objects.filter(id_sales_employee=user)
                if obj.id in [client.company.id for client in clients_handle]:
                    return True
                else:
                    return request.method in SAFE_METHODS
            else:
                return request.method in SAFE_METHODS


class LocationPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not view.detail and user.team == "SU":
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team in ADMIN_TEAM:
            return True
        else:
            if user.team == "SA" or user.team == "SU":
                locations_of_events, locations_of_clients = \
                    get_locations_of_clients_and_events(user)
                if user.team == "SA" \
                        and obj.company in [location.company
                                            for location in locations_of_clients]:
                    return True
                if user.team == "SU" \
                        and obj.id in [location.id
                                       for location in locations_of_events]:
                    return True
                else:
                    return request.method in SAFE_METHODS


class AccountPermission(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
