# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Create your models here.
# class PersonB(User):
#     """Class mère de toutes les class d'individus.
#
#     (clients, prospects, employee_sales, employee_support, employee_manager)
#     """
#     username = models.EmailField(max_length=40, unique=True)
#     # email = username
#
#     phone = models.IntegerField()  # 10 chiffres max. Commencer par 0 possible ?
#     date_updated = models.DateTimeField()
#     pass


class Person(AbstractBaseUser):
    """Class mère de toutes les class d'individus.

    (clients, prospects, employee_sales, employee_support, employee_manager)
    """
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=1_000)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.IntegerField(max_length=10)  # 10 chiffres max. Commencer par 0 possible ?
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=date_created)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
