"""Model de l'app persons.

Client et Prospect héritent tous deux de Persons.
Client et Prospect ne sont pas des comptes utilisateurs.
"""
from django.db import models

from .managers import ClientProspectManager
from accounts.models import Person, SalesTeamEmployee
from additional_data.models import Company


class CommonInfoClientProspect(Person):
    """Model parent aux model Client et Prospect.

    Contient les champs communs aux model Client et Prospect.
    Est un model abstract.
    """

    sales_employee = models.ForeignKey(to=SalesTeamEmployee,
                                       on_delete=models.RESTRICT)
    company = models.ForeignKey(to=Company, on_delete=models.RESTRICT,
                                blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True,
                              verbose_name='email address')

    objects = ClientProspectManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name}"


class Client(CommonInfoClientProspect):
    """Modèle des clients.

    Ayant déjà eu un contrat.
    """

    pass


class Prospect(CommonInfoClientProspect):
    """Modèle des personnes prospectées.

    N'ayant jamais eu de contrat.
    """

    date_last_contact = models.DateTimeField(auto_now=True)
