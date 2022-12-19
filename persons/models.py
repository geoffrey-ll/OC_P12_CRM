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


class ManagerTeamEmployee(Person):
    """Modèle pour les employés de l'équipe de management."""
    account = models.OneToOneField(MyUser, on_delete=models.RESTRICT)

    def save(self, *args, **kwargs):
        self.account.is_admin = True
        self.account.save()
        super().save(*args, **kwargs)


class SalesTeamEmployee(Person):
    """Modèle pour les employés de l'équipe de ventes."""

    account = models.OneToOneField(MyUser, on_delete=models.RESTRICT)

    def save(self, *args, **kwargs):
        self.account.is_admin = False
        self.account.save()
        super().save(*args, **kwargs)


class SupportTeamEmployee(Person):
    """Modèle poure les employés de l'équipe de support."""
    account = models.OneToOneField(MyUser, on_delete=models.RESTRICT)

    def save(self, *args, **kwargs):
        self.account.is_admin = False
        self.account.save()
        super().save(*args, **kwargs)


class Client(Person):
    """Modèle des clients.

    (ayant déjà eu un contrat).
    """
    id_sales_employee = models.ForeignKey(to=SalesTeamEmployee,
                                          on_delete=models.RESTRICT)
    id_company = models.ForeignKey(to=Company, on_delete=models.RESTRICT,
                                   blank=True, null=True)


class Prospect(Person):
    """Modèle des individus prospectés.

    (n'ayant jamais eu de contrat).
    """
    id_company = models.ForeignKey(to=Company, on_delete=models.RESTRICT,
                                   blank=True, null=True)
    id_last_sales_employee_contact = models.ForeignKey(
        to=SalesTeamEmployee, on_delete=models.RESTRICT)
    date_last_contact = models.DateTimeField(auto_now=True) # À modifier car pas vraiment ça


