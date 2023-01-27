from django.contrib.auth.base_user import BaseUserManager


class CompanyManager(BaseUserManager):

    def create(self, siren, name, designation):
        company = self.model(siren=siren, name=name, designation=designation)
        company.save(using=self._db)
        return company


class LocationManager(BaseUserManager):

    def create(
            self, company, nic, designation, street_number, street_name,
            zip_code, town_name, bis_ter="", country=""):

        if country == "":
            country = self.model.COUNTRY_DEFAULT

        location = self.model(
            company=company, nic=nic, designation=designation,
            street_number=street_number, bis_ter=bis_ter,
            street_name=street_name, zip_code=zip_code, town_name=town_name,
            country=country)
        location.save(using=self._db)
        return location
