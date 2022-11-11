from django.db import models

from contracts.models import Contract


# Create your models here.
class Event(models.Model):
    """Modèle d'event."""
    id_contract = models.ForeignKey(to=Contract)
    pass
