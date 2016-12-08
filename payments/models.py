from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

# Create your models here.
from core.models import TimeStampedModel
from payments.card_types import CREDIT_CARD_TYPES
from payments.enums import StatusChoices


class Order(TimeStampedModel):
    """
    defines the order of the services (ex: resume writing, right connect etc)
    For now order does not have any lineitems.
    Each transaction and order is independent
    name: name of the service for which order has to be created
    merch_txn_ref: Unique Merchant Transaction Reference number which is sent to the
    payment server which checkout
    """
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    merch_txn_ref = models.CharField(unique=True, max_length=40, help_text="Merchant Transaction Reference")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    country = CountryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        override save method to create an unique merchant transaction reference
        """
        if self.pk is None:
            from payments.services import generate_unique_transaction_id
            self.merch_txn_ref = generate_unique_transaction_id()
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.merch_txn_ref


class Payment(TimeStampedModel):
    """
    batch_scheduled_date: date at which the actual bank transaction takes place
    status: Pending, rejected, approved depends on the status of the transaction
    status_message: proper message relating to the status
    transaction_no: unique transaction identifier which is used for admin reference
    card_type: card_type of the user
    reciept_no: unique identifier for which is used for the user reference
    """
    batch_scheduled_date = models.DateField(blank=True, null=True)

    STATUS_CHOICES = (
        (StatusChoices.pending.value, 'PENDING'),
        (StatusChoices.failed.value, 'FAILED'),
        (StatusChoices.successful.value, 'APPROVED'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default=StatusChoices.pending.value)
    status_message = models.TextField(null=True, blank=True)
    transaction_num = models.CharField(unique=True, max_length=19, null=True, blank=True,
                                       help_text="Transaction Number")
    card_type = models.CharField(choices=CREDIT_CARD_TYPES, max_length=2, null=True, blank=True)
    receipt_no = models.CharField(unique=True, max_length=12, null=True, blank=True, help_text="Receipt Number")
    order = models.OneToOneField('payments.Order')

    def __unicode__(self):
        return self.order.merch_txn_ref + '-' + self.get_status_display()
