from datetime import timedelta
import glob
import os


from django.core.management import call_command
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

    @staticmethod
    def delete_database():
        database_formats = ["sqlite3"]
        database_files = []
        for db_format in database_formats:
            database_files.extend(glob.glob(f"**/*.{db_format}",
                                            recursive=True))
        for database_file in database_files:
            os.remove(f"{database_file}")

    @staticmethod
    def create_default_superuser():
        Employee.objects.create_superuser(*DEFAULT_SUPERUSER.values())

    @staticmethod
    def create_employees():
        TEAMS_EMPLOYEE = ["manager", "sales", "support"]
        for TEAM in TEAMS_EMPLOYEE:
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

    @staticmethod
    def create_additional_data():
        for i in range(1, 4):
            count = str(i).zfill(2)

            company_name = f"company{count}"
            company_data = {
                "siren": 999_999_999 - i,
                "name": company_name,
                "designation": company_name
            }
            Company.objects.create(*company_data.values())

            location_name = f"location{count}"
            location_data = {
                "company": Company.objects.get(id=i),
                "nic": 99_999 - i,
                "designation": location_name,
                "street_number": i + 1,
                "street_name": f"street{count}",
                "zip_code": 12345,
                "town_name": f"town{count}",
            }
            Location.objects.create(*location_data.values())

    @staticmethod
    def create_clients_and_prospect():
        CATEGORIES = ["client", "prospect"]
        for category in CATEGORIES:
            for i in range(1, 4):
                count = str(i).zfill(2)
                name = f"{category}{count}"

                sales_employees = SalesTeamEmployee.objects.order_by("id")
                data = {
                    "first_name": name,
                    "last_name": name,
                    "phone": 11_23_45_67_89 - i,
                    "sales_employee": sales_employees[i- 1]
                }
                if i // 2 == 0:
                    data["company"] = Company.objects.get(id=i)

                if category == "client":
                    Client.objects.create(*data.values())
                if category == "prospect":
                    Prospect.objects.create(*data.values())

    @staticmethod
    def create_products():
        for i in range(1, 4):
            contract_data = {
                "client": Client.objects.get(id=i),
            }
            Contract.objects.create(*contract_data.values())

            support_employees = SupportTeamEmployee.objects.order_by("id")
            event_data = {
                "support_employee": support_employees[i - 1],
                "contract": Contract.objects.get(id=i),
                "location": Location.objects.get(id=i),
                "end_event": timezone.now() + timedelta(hours=2 + i),
                "attendee": i + 1,
            }
            Event.objects.create(*event_data.values())


    def create_database(self):
        self.create_employees()
        self.create_additional_data()
        self.create_clients_and_prospect()
        self.create_products()

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
                self.style.MIGRATE_HEADING("=> Superuser created : dev\n"))
        else:
            call_command("createsuperuser")
            self.stdout.write(
                self.style.MIGRATE_HEADING("=> Superuser created\n"))

        self.stdout.write(self.style.MIGRATE_HEADING(
            "=> Creation of database in progress\n"))
        self.create_database()
        self.stdout.write(self.style.MIGRATE_HEADING("=> database created"))
