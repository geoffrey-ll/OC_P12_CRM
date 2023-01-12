from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Person, SalesTeamEmployee
from additional_data.models import Company


class Client(Person):
    """Modèle des clients.

    (ayant déjà eu un contrat).
    """
    id_sales_employee = models.ForeignKey(to=SalesTeamEmployee,
                                          on_delete=models.RESTRICT)
    id_company = models.ForeignKey(to=Company, on_delete=models.RESTRICT,
                                   blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Prospect(Person):
    """Modèle des individus prospectés.

    (n'ayant jamais eu de contrat).
    """
    id_company = models.ForeignKey(to=Company, on_delete=models.RESTRICT,
                                   blank=True, null=True)
    id_last_sales_employee_contact = models.ForeignKey(
        to=SalesTeamEmployee, on_delete=models.RESTRICT)
    date_last_contact = models.DateTimeField(auto_now=True) # À modifier car pas vraiment ça


