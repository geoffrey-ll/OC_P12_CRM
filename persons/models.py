from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import PersonManager


# Create your models here.
class Person(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    # password = models.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # is_staff = models.BooleanField()
    # is_active = models.BooleanField()
    # assign_table_team

    objects = PersonManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "phone"]

    # class Meta:
    #     verbose_name = _("user")
    #     verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     return send_mail(subject, message, from_email, [self.email], **kwargs)


class Prospect(models.Model):
    individu = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)