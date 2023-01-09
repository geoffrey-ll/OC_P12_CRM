from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import MyUser
from additional_data.models import Company, Location
from persons.models import (Client, ManagerTeamEmployee, Prospect,
                            SalesTeamEmployee, SupportTeamEmployee)
from products.models import Contract, Event



UserModel = get_user_model()

DEV_USER = {
    "email": "dev@dev.com",
    "team": "WM",
    "password": "dddd__8888"
}

ACCOUNTS = [
    {
        "email": "manager01@manager01.com",
        "team": "MA",
        "password": "manager01manager01"
    },
    {
        "email": "sales01@sales01.com",
        "team": "SA",
        "password": "sales01sales01"
    },
    {
        "email": "support01@support01.com",
        "team": "SU",
        "password": "support01support01"
    }

]

# {
#     "first_name": "",
#     "last_name": "",
#     "phone": "",
#     "account": ""
# }

PERSONS = {
    "manager":
        {
            "first_name": "manager01",
            "last_name": "manager01",
            "phone": "1234567890",
            "account": ""
        },
    "sales":
        {
            "first_name": "sales01",
            "last_name": "sales01",
            "phone": "1234567890",
            "account": ""
        },
    "support":
        {
            "first_name": "support01",
            "last_name": "support01",
            "phone": "1234567890",
            "account": ""
        },
    "client":
        {
            "first_name": "client01",
            "last_name": "client01",
            "phone": "1234567890",
        },
    "prospect":
        {
            "first_name": "prospect01",
            "last_name": "prospect01",
            "phone": "1234567890",
        }
}

COMPANIES = {
        "siren": "123456789",
        "name": "Company01",
    }

LOCATIONS = {
    "nic": 12345,
    "street_number": 1,
    "bis_ter": "ter",
    "street_name": "street01",
    "zip_code": "12345",
    "town_name": "town01"
}


EVENTS = {
}


class Command(BaseCommand):

    help = "Initialize database for local development"

    @staticmethod
    def delete_databse():
        Event.objects.all().delete()
        Contract.objects.all().delete()
        Client.objects.all().delete()
        Prospect.objects.all().delete()
        ManagerTeamEmployee.objects.all().delete()
        SalesTeamEmployee.objects.all().delete()
        SupportTeamEmployee.objects.all().delete()
        MyUser.objects.all().exclude(id=1).delete()
        Location.objects.all().delete()
        Company.objects.all().delete()


    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        self.delete_databse()
        try:
            MyUser.objects.get(email=DEV_USER["email"])
        except:
            UserModel.objects.create_superuser(
                DEV_USER["email"], DEV_USER["team"], DEV_USER["password"])

        for data_accounts in ACCOUNTS:
            MyUser.objects.create(email=data_accounts["email"],
                                  team=data_accounts["team"],
                                  password=data_accounts["password"])

        account_manager = MyUser.objects.filter(team="MA").first()
        account_sales = MyUser.objects.filter(team="SA").first()
        account_support = MyUser.objects.filter(team="SU").first()

        ManagerTeamEmployee.objects.create(
            first_name=PERSONS["manager"]["first_name"],
            last_name=PERSONS["manager"]["last_name"],
            phone=PERSONS["manager"]["phone"], account=account_manager)
        SalesTeamEmployee.objects.create(
            first_name=PERSONS["sales"]["first_name"],
            last_name=PERSONS["sales"]["last_name"],
            phone=PERSONS["sales"]["phone"], account=account_sales)
        SupportTeamEmployee.objects.create(
            first_name=PERSONS["support"]["first_name"],
            last_name=PERSONS["support"]["last_name"],
            phone=PERSONS["support"]["phone"], account=account_support)

        person_sales = SalesTeamEmployee.objects.first()
        person_support = SupportTeamEmployee.objects.first()

        Company.objects.create(siren=COMPANIES["siren"], name=COMPANIES["name"])
        company = Company.objects.first()

        Location.objects.create(id_company=company, nic=LOCATIONS["nic"],
                                designation=company.name,
                                street_number=LOCATIONS["street_number"],
                                bis_ter=LOCATIONS["bis_ter"],
                                street_name=LOCATIONS["street_name"],
                                zip_code=LOCATIONS["zip_code"],
                                town_name=LOCATIONS["town_name"])

        Client.objects.create( first_name=PERSONS["client"]["first_name"],
                               last_name=PERSONS["client"]["last_name"],
                               phone=PERSONS["client"]["phone"],
                               id_sales_employee=person_sales,
                               id_company=company)
        Prospect.objects.create(first_name=PERSONS["prospect"]["first_name"],
                                last_name=PERSONS["prospect"]["last_name"],
                                phone=PERSONS["prospect"]["phone"],
                                id_last_sales_employee_contact=person_sales)

        Contract.objects.create(client=Client.objects.first())
        Event.objects.create(support_employee=person_support,
                             contract=Contract.objects.first(),
                             location=Location.objects.first(),
                             end_event=timezone.now() + timedelta(hours=4),
                             attendees=2)

    print(f"\n\nJe suis bien là\n")