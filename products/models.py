from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from additional_data.models import Location
from persons.models import (Client, SupportTeamEmployee)


class Contract(models.Model):
    id_client = models.ForeignKey(to=Client, on_delete=models.RESTRICT)
    closed = models.BooleanField(default=False)
    # À modifier. Doit être compléter automatiquement. Format : YYMMxxxx où xxxx est ième contract du mois.
    contract_number = models.PositiveIntegerField(unique=True, blank=True,
                                                  null=True)
    amount = models.FloatField(default=0.00)
    payment_due = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Event(models.Model):
    class PossibleStatus(models.IntegerChoices):
        forthcoming = 1, _("Forthcoming")
        in_progress = 2, _("In progress")
        finished = 3, _("Finished")

    id_employee_support = models.ForeignKey(to=SupportTeamEmployee,
                                            on_delete=models.RESTRICT)
    id_contract = models.ForeignKey(to=Contract, on_delete=models.RESTRICT)
    id_location = models.ForeignKey(to=Location, on_delete=models.RESTRICT)
    # doit être automatique selon datetime de l'event.
    status =  models.IntegerField(choices=PossibleStatus.choices)
    # Doit créer un validateur pour empêcher un start_event à une date < à now
    start_event = models.DateTimeField()
    # Doit créer un validateur pour empêcher un end_event < start_event
    end_event = models.DateTimeField()
    attendees = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
