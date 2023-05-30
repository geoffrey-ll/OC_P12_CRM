"""Modèles de l'app products."""
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .errors_messages import MESS_VAL_ERR__END_EVENT_INF_START_EVENT
from .managers import ContractManager, EventManager
from .validators import validate_contract_number_format, validate_datetime_no_past
from accounts.models import SupportTeamEmployee
from additional_data.models import Location
from persons.models import Client


def determine_a_next_contract_number():
    """Génère le prochain numéro de contrat."""
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

    client = models.ForeignKey(to=Client, on_delete=models.RESTRICT)
    closed = models.BooleanField(default=False)
    contract_number = models.PositiveBigIntegerField(
        default=determine_a_next_contract_number, unique=True,
        validators=[validate_contract_number_format])
    amount = models.FloatField(default=0.00)
    payment_due = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = ContractManager()

    def __str__(self):
        return f"Contract n°{self.contract_number}"


class Event(models.Model):

    class PossibleStatus(models.IntegerChoices):

        forthcoming = 1, _("Forthcoming")
        in_progress = 2, _("In progress")
        finished = 3, _("Finished")

    support_employee = models.ForeignKey(to=SupportTeamEmployee,
                                         on_delete=models.RESTRICT)
    contract = models.ForeignKey(to=Contract, on_delete=models.RESTRICT)
    location = models.ForeignKey(to=Location, on_delete=models.RESTRICT)
    status = models.IntegerField(choices=PossibleStatus.choices,
                                 default=PossibleStatus.forthcoming,
                                 editable=False)
    start_event = models.DateTimeField(validators=[validate_datetime_no_past])
    end_event = models.DateTimeField(validators=[validate_datetime_no_past])
    attendees = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2)])
    notes = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = EventManager()

    def clean(self):
        if self.end_event < self.start_event:
            raise ValidationError(message={
                "end_event": _(MESS_VAL_ERR__END_EVENT_INF_START_EVENT)
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
