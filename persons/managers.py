from django.contrib.auth.base_user import BaseUserManager


class ClientProspectManager(BaseUserManager):

    def create(
            self, first_name, last_name, phone, sales_employee, company=None):
        instance = self.model(
            first_name=first_name, last_name=last_name, phone=phone,
            sales_employee=sales_employee, company=company)
        instance.save(using=self._db)
        return instance
