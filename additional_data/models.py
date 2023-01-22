from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Company(models.Model):
    siren = models.PositiveIntegerField(unique=True,
                                        validators=[MinValueValidator(100_000_000),
                                                    MaxValueValidator(999_999_999)])
    name = models.CharField(max_length=50)
    designation = models.CharField(unique=True, default=name, max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.name} (aka: {self.designation})"


class Location(models.Model):
    id_company = models.ForeignKey(to=Company, on_delete=models.RESTRICT)
    nic = models.PositiveIntegerField(validators=[MinValueValidator(10_000),
                                                  MaxValueValidator(99_999)])
    designation = models.CharField(max_length=50, default=id_company.name)
    street_number = models.PositiveSmallIntegerField()
    bis_ter = models.CharField(max_length=10, blank=True, null=True) # Plutôt mettre un choices
    street_name = models.CharField(max_length=50)
    zip_code = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(10000), MaxValueValidator(99999)])
    town_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="France")

    def siret(self):
        """SIRET = SIREN + NIC
        SIRET est unique
        """
        pass

    def __str__(self):
        return f"{self.designation}"