"""Modèles de l'app Products.

classes :
- Contract
- Event

Méthodes :
-

Exceptions :
-

Erreurs :
-
"""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import SupportTeamEmployee
from .errors_messages import MESS_VAL_ERR__END_EVENT_INF_START_EVENT
from .managers import ContractManager, EventManager
from .validators import validate_contract_number_format, validate_datetime_no_past
from additional_data.models import Location
from persons.models import Client


def determine_a_next_contract_number():
    """Identifie le prochain numéro de contrat."""
    now = timezone.now()
    actually_year_month = int(str(now.year) + str(now.month).zfill(2))
    try:
        last_contract_number = Contract.objects.all().filter(
            contract_number__startswith=actually_year_month
        ).order_by("-contract_number")[0].contract_number
        next_number_of_month = int(str(last_contract_number)[-4:]) + 1
    except IndexError:
        next_number_of_month = 1

    next_contract_number = int(str(actually_year_month)
                               + str(next_number_of_month).zfill(4))
    return next_contract_number


class Contract(models.Model):
    """Modèle Contract.

    Variables d'instances :
    - id_client
    - closed
    - contract_number
    - amount
    - payment_due
    - date_created
    - date_updated

    Méthodes :
    - __str__
    """

    client = models.ForeignKey(to=Client, on_delete=models.RESTRICT)
    closed = models.BooleanField(default=False)
    # Doit être complété automatiquement et non seulement suggéré.
    contract_number = models.PositiveSmallIntegerField(
        default=determine_a_next_contract_number, unique=True,
        validators=[validate_contract_number_format])
    amount = models.FloatField(default=0.00)
    payment_due = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = ContractManager()

    def __str__(self):
        """Représentation du modèle dans l'admin Django."""
        return f"Contract n°{self.contract_number}"


class Event(models.Model):
    """Modèle Event.

    Variables d'instances :
    - id_employee_support
    - id_contract
    - id_location
    - status
    - start_event
    - end_event
    - attendees
    - notes
    - date_created
    - date_updated

    Méthodes :
    - clean
    """

    class PossibleStatus(models.IntegerChoices):
        """Choix possibles pour le status."""

        forthcoming = 1, _("Forthcoming")
        in_progress = 2, _("In progress")
        finished = 3, _("Finished")

    support_employee = models.ForeignKey(to=SupportTeamEmployee,
                                         on_delete=models.RESTRICT)
    contract = models.ForeignKey(to=Contract, on_delete=models.RESTRICT)
    location = models.ForeignKey(to=Location, on_delete=models.RESTRICT)
    # doit être automatique selon datetime de l'event.
    status =  models.IntegerField(choices=PossibleStatus.choices,
                                  default=PossibleStatus.forthcoming,
                                  editable=False)
    start_event = models.DateTimeField(default=timezone.now()
                                               + timedelta(hours=2),
                                       validators=[validate_datetime_no_past])
    end_event = models.DateTimeField(validators=[validate_datetime_no_past])
    attendees = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2)])
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = EventManager()

    def clean(self):
        """Validateur du modèle."""
        if self.end_event < self.start_event:
            raise ValidationError(message={
                "end_event": _(MESS_VAL_ERR__END_EVENT_INF_START_EVENT)
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
