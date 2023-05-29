"""Permissions sur les modèles."""
from rest_framework.permissions import BasePermission, SAFE_METHODS

from CRM_EPIC_Events.commons_functions import (get_clients_handle,
                                               get_events_handle)
from CRM_EPIC_Events.settings import ADMIN_TEAM


class ContractPermission(BasePermission):
    """Permissions des contracts.

    - Manager :
        - Afficher, créer, modifier et supprimer.
    - Sales :
        - Afficher et créer.
        - Modifier les contrats des clients dont l'utilisateur a la
        charge.
    - Support :
        - Afficher.
    - Webmaster :
        - Toutes les permissions.
    """

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
                if obj.client.sales_employee.id == user.id:
                    return True
            if user.team == "SU":
                return request.method in SAFE_METHODS


class EventPermission(BasePermission):
    """Permissions des events.

    - Manager :
        - Afficher, créer, modifier et supprimer.
    - Sales :
        - Afficher et créer.
    - Support :
        - Afficher.
        - Modifier des events dont l'utilisateur a la charge.
    - Webmaster :
        - Toutes les permissions.
    """

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
            if user.team == "SA":
                return request.method in SAFE_METHODS
            if user.team == "SU":
                if obj.support_employee.id == user.id:
                    return True


class PersonPermission(BasePermission):
    """Permissions des clients et des prospects.

    Permissions des clients :
    - Manager :
        - Afficher, créer, modifier et supprimer.
    - Sales :
        - Afficher, créer, modifier et supprimer.
    - Support :
        - Afficher.
    - Webmaster :
        - Toutes les permissions.

    Permissions des prospects :
    - Manager :
        - Afficher, créer, modifier et supprimer.
    - Sales :
        - Afficher, créer, modifier et supprimer.
    - Support :
        - Afficher.
    - Webmaster :
        - Toutes les permissions.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.team in ADMIN_TEAM or user.team == "SA":
            return True
        elif user.team == "SU":
            return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team in ADMIN_TEAM:
            return True
        else:
            if user.team == "SA":
                if view.request.query_params.get("prospect") == "True" \
                        or view.request.query_params.get("prospect") == "true":
                    return True
                else:
                    if obj.sales_employee.id == user.id:
                        return True
                    return request.method in SAFE_METHODS
            if user.team == "SU":
                return request.method in SAFE_METHODS


class CompanyPermission(BasePermission):
    """Permissions des companies.

    - Manager :
        - Afficher, créer, modifier et supprimer.
    - Sales :
        - Afficher et créer.
        - Modifier les companies des clients dont l'utilisateur a la
        charge.
    - Support :
        - Afficher.
    - Webmaster :
        - Toutes les permissions.
    """

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
                clients_handle = get_clients_handle(user)
                if obj.id in [client.company.id for client in clients_handle]:
                    return True
                else:
                    return request.method in SAFE_METHODS
            if user.team == "SU":
                return request.method in SAFE_METHODS


class LocationPermission(BasePermission):
    """Permissions des locations.

    - Manager :
        - Afficher, créer, modifier et supprimer.
    - Sales :
        - Afficher et créer.
        - Modifier les locations des clients dont l'utilisateur a la
        charge.
    - Support :
        - Afficher.
        - Modifier les locations des events dont l'utilisateur a la
        charge.
    - Webmaster :
        - Toutes les permissions.
    """

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
            if user.team == "SA":
                clients_handle = get_clients_handle(user)
                if obj.company.id in [client.company.id
                                      for client in clients_handle]:
                    return True
            if user.team == "SU":
                events_handle = get_events_handle(user)
                if obj.id in [event.location.id for event in events_handle]:
                    return True
            return request.method in SAFE_METHODS


class AccountPermission(BasePermission):
    """Permissions des comptes utilisateurs.

    - Manager :
        - Afficher, créer, modifier et supprimer
        (hors comptes Webmaster).
    - Sales :
        - Afficher (hors webmaster).
    - Support :
        - Afficher (hors webmaster).
    - Webmaster :
        - Toutes les permissions.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.team in ADMIN_TEAM:
            return True
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.team in ADMIN_TEAM:
            return True
        return request.method in SAFE_METHODS
