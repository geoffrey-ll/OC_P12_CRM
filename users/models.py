from django.db import models

from persons.models import Person


# Create your models here.
class EmployeeSales(Person):
    pass


class EmployeeSupport(Person):
    pass


class EmployeeManager(Person):
    pass
