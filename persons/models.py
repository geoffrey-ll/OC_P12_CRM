from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import MyUser
from additional_data.models import Company



# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # Doit créer un validateur pour vérifier un format de numéro de téléphone.
    phone = models.PositiveBigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Employee(Person):
    account = models.OneToOneField(MyUser, on_delete=models.RESTRICT)

    # A terme, cette fonction doit être rendu obsolète.
    def save(self, *args, **kwargs):
        if self.account.team == "MA" or self.account.team == "WM":
            self.account.is_admin = True
        else:
            self.account.is_admin = False
        self.account.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{super().__str__()} (id: {self.account.id})"


class ManagerTeamEmployee(Employee):
    """Modèle pour les employés de l'équipe de management."""
    pass


class SalesTeamEmployee(Employee):
    """Modèle pour les employés de l'équipe de ventes."""
    pass


class SupportTeamEmployee(Employee):
    """Modèle poure les employés de l'équipe de support."""
    pass


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


