"""Modèles relatifs aux comptes utilisateurs.

Person : class abstract contenant les champs (hors email) communs aux
    users et aux modèles clients et prospects. C'est deux derniers ne
    sont pas des comptes et ne permettent pas une connexion à l'API.

Employee : Les comptes Webmasters sont enregistrés dans cette table.
    Les autres comptes sont enregistrés dans leur table respective.
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import MyUserManager
from CRM_EPIC_Events.settings import ADMIN_TEAM


class Person(models.Model):
    """Modèle parent aux autres modèles relatifs à des personnes."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name.upper()} {self.first_name}"

    class Meta:
        abstract = True


class Employee(AbstractBaseUser, Person):
    """Modèle user du projet.

    Modèle parent pour les comptes users de l'API.
    """

    class PossibleTeam(models.TextChoices):
        """Ensemble des différents types de comptes possible.

        Chaque compte doit être affecté à l'une de ces team.
        Rôle :
            - Webmaster :
                Non rattaché à la gestion des équipes, des clients et
                des events. Son rôle est l'administration de l'API.
                Il peut être interne ou externe à EPIC EVENTS.
            - Manager :
                Employé de EPIC EVENTS, son rôle est la gestion des
                équipes de ventes (sales) et de support.
            - Sales :
                Employé de EPIC EVENTS, son rôle est la gestion des
                clients et l'acquisition de nouveau clients par
                prospection.
            - Support :
                Employé de EPIC EVENTS, son rôle est la gestion des
                évènements.

        """

        WEBMASTER = "WM", _("Webmaster")
        MANAGER = "MA", _("Manager")
        SALES = "SA", _("Sales")
        SUPPORT = "SU", _("Support")

    email = models.EmailField(max_length=255, unique=True,
                              verbose_name='email address')
    team = models.CharField(choices=PossibleTeam.choices,
                            default=PossibleTeam.SALES, max_length=2)
    # is_staff non nécessaire au projet, mais nécessaire pour Django.
    is_staff = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["team", "first_name", "last_name", "phone"]

    def has_perm(self, perm, obj=None):
        return self.team in ADMIN_TEAM

    def has_module_perms(self, app_label):
        return self.team in ADMIN_TEAM

    def __str__(self):
        return f"{self.id} : {self.email}"


class ManagerTeamEmployee(Employee):
    """Modèle pour la team Manager."""
    pass


class SalesTeamEmployee(Employee):
    """Modèle pour la team Sale."""
    pass


class SupportTeamEmployee(Employee):
    """Modèle pour la team Support."""
    pass
