"""Messages d'erreurs de l'app products."""

FORMAT_CONTRACT_NUMBER = "YYYYMM0000"

MESS_VAL_ERR__CONTRACT_NUMBER_ENDSWITH = \
    f"Incorrect end of the number. For the period concerned (YYMM), " \
    f"a contract cannot have the number 0000. " \
    f"Expected format: {FORMAT_CONTRACT_NUMBER}."
MESS_VAL_ERR__CONTRACT_NUMBER_LEN = f"Incorrect length. Expected format: " \
                                   f"{FORMAT_CONTRACT_NUMBER}."
MESS_VAL_ERR__CONTRACT_NUMBER_STARTSWITH = \
    f"Incorrect start of the number. The current year or month is different. " \
    f"Expected format: {FORMAT_CONTRACT_NUMBER}."
MESS_VAL_ERR__DATETIME_PAST = "%(value)s Has already passed. To indicate a " \
                              "moment to come."
MESS_VAL_ERR__END_EVENT_INF_START_EVENT = \
    "The end of the event cannot be earlier than the beginning of the event."
