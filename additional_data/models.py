"""Model de l'app additional_data."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from .managers import CompanyManager, LocationManager


class Company(models.Model):

    siren = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(100_000_000), MaxValueValidator(999_999_999)
        ])
    name = models.CharField(max_length=50)
    designation = models.CharField(unique=True, default=name, max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CompanyManager()

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.name} (aka: {self.designation})"


class Location(models.Model):

    COUNTRY_DEFAULT = "France"

    company = models.ForeignKey(to=Company, on_delete=models.RESTRICT)
    nic = models.PositiveIntegerField(validators=[MinValueValidator(10_000),
                                                  MaxValueValidator(99_999)])
    designation = models.CharField(max_length=50, default=company.name)
    street_number = models.PositiveSmallIntegerField()
    bis_ter = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=50)
    zip_code = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(10_000), MaxValueValidator(99_999)])
    town_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default=COUNTRY_DEFAULT)

    objects = LocationManager()

    def __str__(self):
        return f"{self.designation}"
