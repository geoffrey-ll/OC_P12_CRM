from django.contrib.auth.base_user import BaseUserManager


def determine_is_admin_status(team):
    if team == "MA" or team == "WM":
        return True
    else:
        return False


class MyUserManager(BaseUserManager):

    def create_user(
            self, email, team, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not team:
            raise ValueError("Users must have a team")

        user = self.model(
            email=self.normalize_email(email), team=team,
            first_name=first_name, last_name=last_name, phone=phone)

        user.is_admin = determine_is_admin_status(user.team)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email, team, first_name, last_name, phone, password=None):
        user = self.create_user(
            email, team=team, password=password,
            first_name=first_name, last_name=last_name, phone=phone)

        user.save(using=self._db)
        return user
