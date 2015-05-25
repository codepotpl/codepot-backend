import datetime
from enum import Enum

from django.db import models

from codepot import (
    create_hash,
    enum_to_model_choices,
)


class TicketTypeName(Enum):
    FIRST_DAY = 'FIRST_DAY'
    SECOND_DAY = 'SECOND_DAY'
    BOTH_DAYS = 'BOTH_DAYS'

class Ticket(models.Model):
    ticket_id = models.CharField(primary_key=True, max_length=32, default=create_hash)
    purchase = models.ForeignKey('codepot.Purchase')
    created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    type = models.CharField(max_length=64, choices=enum_to_model_choices(TicketTypeName), null=False, blank=False)

    def __str__(self):
        return 'Ticket {} / {}'.format(self.purchase_id, self.user.id)
