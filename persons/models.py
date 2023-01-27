from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import ClientProspectManager
from accounts.models import Person, SalesTeamEmployee
from additional_data.models import Company



class CommonInfoClientProspect(Person):

    sales_employee = models.ForeignKey(to=SalesTeamEmployee,
                                       on_delete=models.RESTRICT)
    company = models.ForeignKey(to=Company, on_delete=models.RESTRICT,
                                blank=True, null=True)

    objects = ClientProspectManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name}"


class Client(CommonInfoClientProspect):
    """Modèle des clients.

    (ayant déjà eu un contrat).
    """
    pass


class Prospect(CommonInfoClientProspect):
    """Modèle des individus prospectés.

    (n'ayant jamais eu de contrat).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self._meta.get_field("sales_employee")
        field.verbose_name = "last sales contacted"

    last_sales_contacted = CommonInfoClientProspect.sales_employee
    date_last_contact = models.DateTimeField(auto_now=True) # À modifier car pas vraiment ça


