from django.shortcuts import get_object_or_404

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received

from payments.models import Order


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print "valid signal called"

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        invoice_id = ipn_obj.invoice
        order = get_object_or_404(Order, merch_txn_ref=invoice_id)
        order.paid = True
        order.save()
        # if ipn_obj.receiver_email != order.user.email:
        #     print "not a valid payment"
        #     # Not a valid payment
        #     return


        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            print "user paid"
    else:
        print "payment not completed"

def invalid_money(sender, **kwargs):
    ipn_obj = sender
    print "invalid money"

invalid_ipn_received.connect(invalid_money)
valid_ipn_received.connect(show_me_the_money)
