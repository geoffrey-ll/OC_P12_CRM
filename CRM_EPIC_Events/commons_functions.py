"""Fonctions communes à plusieurs modules."""
from accounts.models import Employee
from additional_data.models import Location
from persons.models import Client
from products.models import Event


def get_clients_handle(user):
    """Return les clients gérés par le sale employee."""
    return Client.objects.filter(sales_employee=user)


def get_events_of_clients_handle(clients_handle):
    """Return les events des clients gérés par le sale employee."""
    return Event.objects.filter(
        contract__client__in=[client for client in clients_handle])


def get_supports_of_clients_handle(user):
    """
        Return les supports employees qui gèrent les events des clients
        du sale employee.
    """
    clients_handle = get_clients_handle(user)
    events_clients = get_events_of_clients_handle(clients_handle)
    return Employee.objects.filter(
        id__in=[event.support_employee.id for event in events_clients])


def get_events_handle(user):
    """Return les events gérés par le support employee."""
    return Event.objects.filter(support_employee=user)


def get_clients_of_events_handle(events_handle):
    """Return les clients des events gérés par le support employee."""
    return Client.objects.filter(
        id__in=[event.contract.client.id for event in events_handle])


def get_sales_of_events_handle(user):
    """
    Return les sales employees qui gèrent les clients des events du
    support employee.
    """
    events_handle = get_events_handle(user)
    clients_events = get_clients_of_events_handle(events_handle)
    return Employee.objects.filter(
        id__in=[client.sales_employee.id for client in clients_events])


def get_locations_of_clients_and_of_events(user):
    """Return les locations des events et des clients gérés par user.
    """
    clients = []
    events = []
    if user.team == "SA":
        clients = get_clients_handle(user)
        events = get_events_of_clients_handle(clients)
    elif user.team == "SU":
        events = get_events_handle(user)
        clients = get_clients_of_events_handle(events)

    locations_of_events = Location.objects.filter(
        id__in=[event.location.id for event in events])
    locations_of_clients = Location.objects.filter(
        company__in=[client.company for client in clients])
    return locations_of_events | locations_of_clients
