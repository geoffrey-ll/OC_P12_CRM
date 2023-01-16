import glob
import os
import sys

from django.core.management import call_command, execute_from_command_line
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from CRM_EPIC_Events.settings import PROJECT_APPS
from accounts.models import Employee, ManagerTeamEmployee, SupportTeamEmployee, SalesTeamEmployee
from additional_data.models import Company, Location
from persons.models import (Client, Prospect)
from products.models import Contract, Event


Employee = get_user_model()


DEFAULT_SUPERUSER = {
    "email": "dev@dev.com",
    "team": "WM",
    "first_name": "dev",
    "last_name": "dev",
    "phone": 1234567890,
    "password": "dddd__8888"
}


class Command(BaseCommand):

    help = "Initialise a database for test development."

    def add_arguments(self, parser):
        parser.add_argument("--default", action="store_true",
                            help="Create the default superuser : dev.")

    @staticmethod
    def delete_migrations():
        for app in PROJECT_APPS:
            path_migrations_dir = f"{app}/migrations"
            if os.path.exists(path_migrations_dir):
                migrations_files = glob.glob(f"{path_migrations_dir}/*.py")
                for migration_file in migrations_files:
                    if migration_file != f"{path_migrations_dir}/__init__.py":
                        os.remove(f"{migration_file}")
        # print(f"=> Migrations deleted")

    @staticmethod
    def delete_database():
        database_formats = ["sqlite3"]
        database_files = []
        for db_format in database_formats:
            database_files.extend(glob.glob(f"**/*.{db_format}",
                                            recursive=True))
        for database_file in database_files:
            os.remove(f"{database_file}")
        # print(f"=> Database deleted")

    @staticmethod
    def create_default_superuser():
        Employee.objects.create_superuser(*DEFAULT_SUPERUSER.values())

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        self.delete_migrations()
        self.stdout.write(self.style.MIGRATE_HEADING("=> Migrations deleted\n"))
        self.delete_database()
        self.stdout.write(self.style.MIGRATE_HEADING("=> Database deleted\n"))
        call_command("makemigrations")
        self.stdout.write(self.style.MIGRATE_HEADING("=> Makemigrations: ok\n"))
        call_command("migrate")
        self.stdout.write(self.style.MIGRATE_HEADING("=> Migrate: ok\n"))
        if options["default"]:
            self.create_default_superuser()
            self.stdout.write(
                self.style.MIGRATE_HEADING("=> Superuser dev created"))
            # call_command("createsuperuser",
            #     email=SUPERUSER["email"],
            #     team=SUPERUSER["team"], first_name=SUPERUSER["first_name"],
            #     last_name=SUPERUSER["last_name"], phone=SUPERUSER["phone"]
            # )
        else:
            call_command("createsuperuser")
            self.stdout.write(
                self.style.MIGRATE_HEADING("=> Superuser created"))



# ACCOUNTS = [
#     {
#         "email": "manager01@manager01.com",
#         "team": "MA",
#         "password": "manager01manager01",
#         "first_name": "manager01",
#         "last_name": "manager01",
#         "phone": "1234567890"
#     },
#     {
#         "email": "sales01@sales01.com",
#         "team": "SA",
#         "password": "sales01sales01",
#         "first_name": "sales01",
#         "last_name": "sales01",
#         "phone": "1234567890"
#     },
#     {
#         "email": "support01@support01.com",
#         "team": "SU",
#         "password": "support01support01",
#         "first_name": "support01",
#         "last_name": "support01",
#         "phone": "1234567890"
#     }
#
# ]
#
#
# PERSONS = {
#     "manager":
#         {
#             "first_name": "manager01",
#             "last_name": "manager01",
#             "phone": "1234567890",
#             "account": ""
#         },
#     "sales":
#         {
#             "first_name": "sales01",
#             "last_name": "sales01",
#             "phone": "1234567890",
#             "account": ""
#         },
#     "support":
#         {
#             "first_name": "support01",
#             "last_name": "support01",
#             "phone": "1234567890",
#             "account": ""
#         },
#     "client":
#         {
#             "first_name": "client01",
#             "last_name": "client01",
#             "phone": "1234567890",
#         },
#     "prospect":
#         {
#             "first_name": "prospect01",
#             "last_name": "prospect01",
#             "phone": "1234567890",
#         }
# }
#
# COMPANIES = {
#         "siren": "123456789",
#         "name": "Company01",
#     }
#
# LOCATIONS = {
#     "nic": 12345,
#     "street_number": 1,
#     "bis_ter": "ter",
#     "street_name": "street01",
#     "zip_code": "12345",
#     "town_name": "town01"
# }
#
#
# EVENTS = {
# }
#
#
# class Command(BaseCommand):
#
#     help = "Initialize database for local development"
#
#     @staticmethod
#     def delete_databse():
#         Event.objects.all().delete()
#         Contract.objects.all().delete()
#         Client.objects.all().delete()
#         Prospect.objects.all().delete()
#         ManagerTeamEmployee.objects.all().delete()
#         SalesTeamEmployee.objects.all().delete()
#         SupportTeamEmployee.objects.all().delete()
#         Employee.objects.all().exclude(id=1).delete()
#         Location.objects.all().delete()
#         Company.objects.all().delete()
#
#
#     def handle(self, *args, **options):
#         self.stdout.write(self.style.MIGRATE_HEADING(self.help))
#         self.delete_databse()
#         try:
#             Employee.objects.get(email=DEV_USER["email"])
#         except:
#             UserModel.objects.create_superuser(
#                 DEV_USER["email"], DEV_USER["team"],
#                 DEV_USER["first_name"], DEV_USER["last_name"], DEV_USER["phone"],
#                 DEV_USER["password"])
#
#         for data_accounts in ACCOUNTS:
#             Employee.objects.create(email=data_accounts["email"],
#                                     team=data_accounts["team"],
#                                     first_name=data_accounts["first_name"],
#                                     last_name=data_accounts["last_name"],
#                                     phone=data_accounts["phone"],
#                                     password=data_accounts["password"])
#
#         # account_manager = Employee.objects.filter(team="MA").first()
#         # account_sales = Employee.objects.filter(team="SA").first()
#         # account_support = Employee.objects.filter(team="SU").first()
#
#         ManagerTeamEmployee.objects.create()
#             # first_name=PERSONS["manager"]["first_name"],
#             # last_name=PERSONS["manager"]["last_name"],
#             # phone=PERSONS["manager"]["phone"])#, account=account_manager)
#         SalesTeamEmployee.objects.create()
#             # first_name=PERSONS["sales"]["first_name"],
#             # last_name=PERSONS["sales"]["last_name"],
#             # phone=PERSONS["sales"]["phone"])#, account=account_sales)
#         SupportTeamEmployee.objects.create()
#             # first_name=PERSONS["support"]["first_name"],
#             # last_name=PERSONS["support"]["last_name"],
#             # phone=PERSONS["support"]["phone"])#, account=account_support)
#
#         person_sales = SalesTeamEmployee.objects.first()
#         person_support = SupportTeamEmployee.objects.first()
#
#         Company.objects.create(siren=COMPANIES["siren"], name=COMPANIES["name"])
#         company = Company.objects.first()
#
#         Location.objects.create(id_company=company, nic=LOCATIONS["nic"],
#                                 designation=company.name,
#                                 street_number=LOCATIONS["street_number"],
#                                 bis_ter=LOCATIONS["bis_ter"],
#                                 street_name=LOCATIONS["street_name"],
#                                 zip_code=LOCATIONS["zip_code"],
#                                 town_name=LOCATIONS["town_name"])
#
#         Client.objects.create( first_name=PERSONS["client"]["first_name"],
#                                last_name=PERSONS["client"]["last_name"],
#                                phone=PERSONS["client"]["phone"],
#                                id_sales_employee=person_sales,
#                                id_company=company)
#         Prospect.objects.create(first_name=PERSONS["prospect"]["first_name"],
#                                 last_name=PERSONS["prospect"]["last_name"],
#                                 phone=PERSONS["prospect"]["phone"],
#                                 id_last_sales_employee_contact=person_sales)
#
#         Contract.objects.create(client=Client.objects.first())
#         Event.objects.create(support_employee=person_support,
#                              contract=Contract.objects.first(),
#                              location=Location.objects.first(),
#                              end_event=timezone.now() + timedelta(hours=4),
#                              attendees=2)
#
#     print(f"\n\nJe suis bien là\n")