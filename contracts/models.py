from django.db import models


# Create your models here.
class Contract(models.Model):
    contract_number = models.PositiveBigIntegerField()
    pass
