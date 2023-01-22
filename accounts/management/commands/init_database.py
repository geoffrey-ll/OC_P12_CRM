import glob
import os
import sys
import subprocess

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

DATA_FOR_DEVELOPMENT = {
    "accounts": {
        "manager": {
            "email": ["manager01@manager01.com", "manager02@manager02.com", "manager03@manager03.com"],
        },
        "sales": {

        },
        "support": {

        }
    },
    "persons": {
        "client": {

        },
        "prospect": {

        }
    },
    "products": {
        "contract": {

        },
        "event": {

        }
    },
    "additional_data": {
        "company": {

        },
        "location": {

        }
    },
    "key": {}
}

DATA_COMPANIES = {
    "siren": [123456789, 123456788, 123456787],
    "name": ["company01", "company02", "company03"],
    "designation": ["company01", "company02", "company03"]
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

    @staticmethod
    def create_employees():
        TEAM_EMPLOYEE = ["manager", "sales", "support"]
        for TEAM in TEAM_EMPLOYEE:
            for i in range(1, 4):
                count = str(i).zfill(2)
                name = f"{TEAM}{count}"
                data = {
                    "email": f"{name}@{name}.com",
                    "team": f"{TEAM[0:2].upper()}",
                    "first_name": f"{name}",
                    "last_name": f"{name}",
                    "phone": 1234567890,
                    "password": f"{name*4}"
                }
                if TEAM == "manager":
                    ManagerTeamEmployee.objects.create_user(*data.values())
                elif TEAM == "sales":
                    SalesTeamEmployee.objects.create_user(*data.values())
                elif TEAM == "support":
                    SupportTeamEmployee.objects.create_user(*data.values())

    # @staticmethod
    # def create_additional_data():
    #     for i in range(1, 4):
    #         count = str(i).zfill(2)
    #         name = f"company{count}"
    #         data = {
    #             "siren": 999999999 - i,
    #             "name": name,
    #             "designation": name
    #         }
    #         Company.objects.create(*data.values())

    def create_database(self):
        self.create_employees()
        # self.create_additional_data()
        # self.create.persons()

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
                self.style.MIGRATE_HEADING("=> Superuser created : dev"))
            # call_command("createsuperuser",
            #              f"{DEFAULT_SUPERUSER.keys()}"=DEFAULT_SUPERUSER.values())
            # call_command("createsuperuser",
            #              *DEFAULT_SUPERUSER.keys(), **DEFAULT_SUPERUSER.values())
        else:
            call_command("createsuperuser")
            self.stdout.write(
                self.style.MIGRATE_HEADING("=> Superuser created"))

        self.create_database()


        # call_command("runserver")



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