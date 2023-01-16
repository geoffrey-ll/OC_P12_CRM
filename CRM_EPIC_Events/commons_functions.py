from CRM_EPIC_Events.settings import DATETIME_FORMAT


def datetime_to_representation(datetime):
    return datetime.strftime(DATETIME_FORMAT)
