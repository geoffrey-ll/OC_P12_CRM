"""Commande d'automatisation de database.

Pendant le développement du projet avec database sqlite3.
Commande permettant d'automatiser le processus pour créer une nouvelle
database sqlite3.

Étapes :
- Suppression des migrations et de la database.
- Création des migrations.
- Création d'une database en sqlite3.
"""
from datetime import timedelta
import glob
import os

from decouple import config
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from CRM_EPIC_Events.settings import PROJECT_APPS
from accounts.models import (Employee, ManagerTeamEmployee,
                             SupportTeamEmployee, SalesTeamEmployee)
from additional_data.models import Company, Location
from persons.models import (Client, Prospect)
from products.models import Contract, Event


Employee = get_user_model()

DEFAULT_SUPERUSER = {
    "email": config("SUPERUSER_DEFAULT_EMAIL"),
    "team": "WM",
    "first_name": config("SUPERUSER_DEFAULT_FIRST_NAME"),
    "last_name": config("SUPERUSER_DEFAULT_LAST_NAME"),
    "phone": config("SUPERUSER_DEFAULT_PHONE"),
    "password": config("SUPERUSER_DEFAULT_PASSWORD")
}


class Command(BaseCommand):
    """Commande ajoutée à manage.py

    Pour créer automatiquement une database en sqlite3.
    """

    help = "Initialise a database for test development."

    def add_arguments(self, parser):
        """Argument de commande.

        L'argument --default permet de générer le superuser par défaut
        en même temps que le reste de la database.
        """
        parser.add_argument("--default", action="store_true",
                            help="Create the default superuser : dev.")

    @staticmethod
    def delete_migrations():
        """Suppression des migrations."""
        for app in PROJECT_APPS:
            path_migrations_dir = f"{app}/migrations"
            if os.path.exists(path_migrations_dir):
                migrations_files = glob.glob(f"{path_migrations_dir}/*.py")
                for migration_file in migrations_files:
                    if migration_file != f"{path_migrations_dir}/__init__.py":
                        os.remove(f"{migration_file}")

    @staticmethod
    def delete_database():
        """Suppression database."""
        database_formats = ["sqlite3"]
        database_files = []
        for db_format in database_formats:
            database_files.extend(glob.glob(f"**/*.{db_format}",
                                            recursive=True))
        for database_file in database_files:
            os.remove(f"{database_file}")

    @staticmethod
    def create_default_superuser():
        """Création superuser par défaut."""
        Employee.objects.create_superuser(*DEFAULT_SUPERUSER.values())

    @staticmethod
    def create_employees():
        """Création de 3 employés de chaque team."""
        teams_employee = ["manager", "sales", "support"]
        for team in teams_employee:
            for i in range(1, 4):
                count = str(i).zfill(2)
                name = f"{team}{count}"
                data = {
                    "email": f"{name}@{name}.com",
                    "team": f"{team[0:2].upper()}",
                    "first_name": f"{name}",
                    "last_name": f"{name}",
                    "phone": 1234567890,
                    "password": f"{name*4}"
                }
                if team == "manager":
                    ManagerTeamEmployee.objects.create_user(*data.values())
                elif team == "sales":
                    SalesTeamEmployee.objects.create_user(*data.values())
                elif team == "support":
                    SupportTeamEmployee.objects.create_user(*data.values())

    @staticmethod
    def create_additional_data():
        """Création de 3 locations et 3 companies."""
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
        """Création de 3 clients et de 3 prospects."""
        categories = ["client", "prospect"]
        for category in categories:
            for i in range(1, 4):
                count = str(i).zfill(2)
                name = f"{category}{count}"

                sales_employees = SalesTeamEmployee.objects.order_by("id")
                data = {
                    "first_name": name,
                    "last_name": name,
                    "phone": 11_23_45_67_89 - i,
                    "sales_employee": sales_employees[i - 1]
                }
                if i // 2 == 0:
                    data["company"] = Company.objects.get(id=i)

                if category == "client":
                    Client.objects.create(*data.values())
                if category == "prospect":
                    Prospect.objects.create(*data.values())

    @staticmethod
    def create_products():
        """Création de 3 contracts et de 3 events."""
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
        """Création de la database."""
        self.create_employees()
        self.create_additional_data()
        self.create_clients_and_prospect()
        self.create_products()

    def handle(self, *args, **options):
        """Le main de la commande."""
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
