"""Manager de l'app persons."""
from django.contrib.auth.base_user import BaseUserManager


class ClientProspectManager(BaseUserManager):
    """Manager communs aux model Client et Prospect."""

    def create(
            self, first_name, last_name, phone, sales_employee, email,
            company=None):

        persons = self.model(
            first_name=first_name, last_name=last_name, phone=phone,
            sales_employee=sales_employee, email=email, company=company)
        persons.save(using=self._db)
        return persons
