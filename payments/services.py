from datetime import datetime

from django.shortcuts import get_object_or_404
import jwt

from core.models import Service
from payments.enums import StatusChoices
from payments.migs_mastercard import MigsClient
from payments.models import Order, Payment

PaymentStatus = {
    '0': 'Transaction Successful',
    '1': 'Unknown Error',
    '2': 'Bank Declined Transaction',
    '3': 'No Reply from Bank',
    '4': 'Expired Card',
    '5': 'Insufficient Funds',
    '6': 'Error Communicating with Bank',
    '7': 'Payment Server System Error',
    '8': 'Transaction Type Not Supported',
    '9': 'Bank declined transaction (Do not contact Bank)',
    'A': 'Transaction Aborted',
    'C': 'Transaction Cancelled',
    'D': 'Deferred transaction has been received and is awaiting processing',
    'F': '3D Secure Authentication failed',
    'I': 'Card Security Code verification failed',
    'L': 'Shopping Transaction Locked (Please try the transaction again later)',
    'N': 'Cardholder is not enrolled in Authentication Scheme',
    'P': 'Transaction has been received by the Payment Adaptor and is being processed',
    'R': 'Transaction was not processed - Reached limit of retry attempts allowed',
    'S': 'Duplicate SessionID (OrderInfo)',
    'T': 'Address Verification Failed',
    'U': 'Card Security Code Failed',
    'V': 'Address Verification and Card Security Code Failed',
    '?': 'Transaction status is unknown'
}


def generate_unique_merch_txn_ref():
    unique_no = datetime.now().strftime(("%f%d%m%Y%S%M%H"))
    unique_order_id = jwt.encode({}, unique_no, algorithm='HS256')[-20:].upper()
    return "ORDER" + "-" + unique_order_id


def place_order_for_user(user, service, amount, country_code):
    order = Order.objects.create(user=user, title=service.name,
                                 amount=amount, country=country_code)
    Payment.objects.create(order=order)
    return order


def get_payment_gateway_url(user, amount, service, country_code):
    order = place_order_for_user(user, service, amount, country_code)
    merchant_transaction_ref = order.merch_txn_ref
    migs_client = MigsClient(merchant_transaction_ref, amount)
    payment_gateway_url = migs_client.generate_payment_url()
    return payment_gateway_url


def _get_order_and_payment(callback_data, user):
    merch_txn_ref = callback_data.get('vpc_MerchTxnRef')
    order = get_object_or_404(Order, user=user, merch_txn_ref=merch_txn_ref)
    payment = order.payment
    return order, payment


def _update_payment(callback_data, payment):
    response_code = callback_data.get('vpc_TxnResponseCode', None)
    batch_no = callback_data.get('vpc_BatchNo', None)
    payment.batch_scheduled_date = datetime.strptime(batch_no, '%Y%M%d') if batch_no else None
    payment.status_message = callback_data.get('vpc_Message', None)
    payment.transaction_num = callback_data.get('vpc_TransactionNo', None)
    payment.card_type = callback_data.get('vpc_card', None)
    payment.receipt_no = callback_data.get('vpc_ReceiptNo', None)
    if response_code == '0':
        payment.status = StatusChoices.successful.value
    else:
        payment.status = StatusChoices.failed.value
    payment.save()
    return payment


def update_user_payment(user, callback_data):
    order, payment = _get_order_and_payment(callback_data, user)
    payment = _update_payment(callback_data, payment)
    return payment


def remove_secure_hash_from_payload(payment_payload):
    response_secure_hash = payment_payload.pop('vpc_SecureHash')
    return response_secure_hash, payment_payload


def validate_payment_payload(payment_payload):
    payment_payload = payment_payload.dict()
    migs_client = MigsClient(None, None)
    if 'vpc_SecureHash' in payment_payload:
        response_secure_hash, payment_payload = remove_secure_hash_from_payload(payment_payload)
        actual_secure_hash = migs_client.hash_all_fields(payment_payload)
        if response_secure_hash == actual_secure_hash:
            is_valid = True
        else:
            is_valid = False
    else:
        is_valid = False
    return is_valid


def get_service(service_nk):
    service = get_object_or_404(Service, nk=service_nk)
    return service
