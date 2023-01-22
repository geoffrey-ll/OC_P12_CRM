from CRM_EPIC_Events.settings import DATETIME_FORMAT
from additional_data.models import Location
from persons.models import Client
from products.models import Event


def datetime_to_representation(datetime):
    return datetime.strftime(DATETIME_FORMAT)


def get_clients_handle(user):
    return Client.objects.filter(id_sales_employee=user)


def get_events_of_clients_handle(clients_handle):
    return Event.objects.filter(contract__client__in=[
        client for client in clients_handle])


def get_events_handle(user):
    return Event.objects.filter(support_employee=user)


def get_clients_of_events_handle(events_handle):
    return Client.objects.filter(
        id__in=[event.contract.client.id for event in events_handle])


def get_locations_of_clients_and_events(user):
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
        id_company__in=[client.id_company for client in clients])
    return locations_of_events, locations_of_clients
