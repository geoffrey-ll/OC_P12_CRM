"""Validateurs personnalisés du modèle Event.

classes :
-

Méthodes :
- validate_datetime_no_past
- validate_contract_number_format
-

Exceptions :
-

Erreurs :
-
"""

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .errors_messages import (MESS_VAL_ERR__DATETIME_PAST,
                              MESS_VAL_ERR__CONTRACT_NUMBER_ENDSWITH,
                              MESS_VAL_ERR__CONTRACT_NUMBER_LEN,
                              MESS_VAL_ERR__CONTRACT_NUMBER_STARTSWITH)


def validate_datetime_no_past(value):
    """

    :param value:
    :return:
    """
    if value < timezone.now():
        raise ValidationError(_(MESS_VAL_ERR__DATETIME_PAST),
                              params={"value": value},)


def validate_contract_number_format(value):
    """Vérifie le format du numéro de contrat."""
    str_contract_number = str(value)

    def validate_endswith_contract_number(contract_number_of_month):
        """Vérifie que le numéro de contrat ne termine pas par 0000."""
        if contract_number_of_month == "0000":
            return ValidationError(MESS_VAL_ERR__CONTRACT_NUMBER_ENDSWITH)
        return ""

    def validate_len_contract_number():
        """Vérifie la longueur du numéro du contrat."""
        if len(str_contract_number) != 10:
            return ValidationError(MESS_VAL_ERR__CONTRACT_NUMBER_LEN)
        return ""

    def validate_startswith_contract_number(year_month_of_contract_number):
        """Vérifie que le numéro de contrat commence par YYYYMM en cours."""
        now = timezone.now()
        actually_year_month = str(now.year) + str(now.month).zfill(2)
        if year_month_of_contract_number != actually_year_month:
            return ValidationError(MESS_VAL_ERR__CONTRACT_NUMBER_STARTSWITH)
        return ""

    error_len = validate_len_contract_number()
    error_startswith = validate_startswith_contract_number(str_contract_number[:6])
    error_endswith = validate_endswith_contract_number(str_contract_number[-4:])

    errors = []
    if error_len != "":
        errors.append(error_len)
    if error_startswith != "":
        errors.append(error_startswith)
    if error_endswith != "":
        errors.append(error_endswith)
    raise ValidationError(errors)
