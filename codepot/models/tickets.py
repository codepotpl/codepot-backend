from django.db import models

from codepot import create_hash


class Ticket(models.Model):
    ticket_id = models.CharField(primary_key=True, max_length=32, default=create_hash)
    purchase = models.ForeignKey('codepot.Purchase')

    def __str__(self):
        return 'Ticket {} / {}'.format(self.purchase_id, self.user.id)
