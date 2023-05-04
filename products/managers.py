from django.contrib.auth.base_user import BaseUserManager


class ContractManager(BaseUserManager):

    def create(self, client, *args, **kwargs):
        contract = self.model(client=client, *args, **kwargs)
        contract.save(using=self._db)
        return contract


class EventManager(BaseUserManager):

    def create(
            self, support_employee, contract, location, start_event, end_event, attendees, notes, *args, **kwargs):
        event = self.model(
            support_employee=support_employee, contract=contract,
            location=location, start_event=start_event, end_event=end_event, attendees=attendees, notes=notes, *args, **kwargs)
        event.save(using=self._db)
        return event
