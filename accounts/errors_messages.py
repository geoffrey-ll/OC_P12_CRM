"""Messages d'erreurs de l'app accounts."""
MESS_ERROR_CHANGE_TEAM_MA = \
    f"Impossible to change teams. Your account is registered as manager " \
    f"employee (ForeignKey) on other data."
MESS_ERROR_CHANGE_TEAM_SA = \
    f"Impossible to change teams. Your account is registered as sale " \
    f"employee (ForeignKey) on other data."
MESS_ERROR_CHANGE_TEAM_SU = \
    f"Impossible to change teams. Your account is registered as support " \
    f"employee (ForeignKey) on other data."
mess_errors_change_teams = [MESS_ERROR_CHANGE_TEAM_MA,
                            MESS_ERROR_CHANGE_TEAM_SA,
                            MESS_ERROR_CHANGE_TEAM_SU]
