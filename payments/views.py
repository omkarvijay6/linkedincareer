import hashlib
import requests

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf

# Create your views here.
from core.models import Service
from payments.enums import StatusChoices
from payments.payumoney import generate_payumoney_post_data
from payments.services import get_payment_gateway_url, update_user_payment, validate_payment_payload, get_service, \
    place_order_for_user


def payment_callback(request):
    payment_payload = request.GET
    user = request.user
    secure_is_valid = validate_payment_payload(payment_payload)
    if secure_is_valid:
        payment = update_user_payment(user, payment_payload)
        if payment.status == StatusChoices.successful.value:
            redirect_url = reverse('payment_successful')
        else:
            redirect_url = reverse('payment_failed')
    else:
        redirect_url = reverse('forbidden')
    return HttpResponseRedirect(redirect_url)


@login_required
def redirect_to_payment_gateway(request, amount, service_nk, country_code=None):
    user = request.user
    service = get_service(service_nk)
    payment_gateway_url = get_payment_gateway_url(user, amount, service, country_code)
    return redirect(payment_gateway_url)

@login_required
def payumoney_payment(request, amount, service_nk, country_code=None):
    user = request.user
    service = get_service(service_nk)
    order = place_order_for_user(user, service, amount, country_code)
    transaction_id = order.merch_txn_ref
    payumoney_post_data, payumoney_url = generate_payumoney_post_data(user, service, transaction_id)
    response = requests.post(payumoney_url, data=payumoney_post_data)
    return HttpResponseRedirect(response.url)


def Home(request):
    MERCHANT_KEY = "rjQUPktU"
    key = "rjQUPktU"
    SALT = "e5iIg1jwi8"
    PAYU_BASE_URL = "https://test.payu.in/_payment"
    action = ''
    posted = {}
    for i in request.POST:
        posted[i] = request.POST[i]
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid = hash_object.hexdigest()[0:20]
    hashh = ''
    posted['txnid'] = txnid
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = key
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    hashh = hashlib.sha512(hash_string).hexdigest().lower()
    action = PAYU_BASE_URL
    if (posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get(
            "firstname") != None and posted.get("email") != None):
        return render_to_response('current_datetime.html', RequestContext(request, {"posted": posted, "hashh": hashh,
                                                                                    "MERCHANT_KEY": MERCHANT_KEY,
                                                                                    "txnid": txnid,
                                                                                    "hash_string": hash_string,
                                                                                    "action": "https://test.payu.in/_payment"}))
    else:
        return render_to_response('current_datetime.html', RequestContext(request, {"posted": posted, "hashh": hashh,
                                                                                    "MERCHANT_KEY": MERCHANT_KEY,
                                                                                    "txnid": txnid,
                                                                                    "hash_string": hash_string,
                                                                                    "action": "."}))


@csrf_protect
@csrf_exempt
def success(request):
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "e5iIg1jwi8"
    import ipdb;ipdb.set_trace()
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq).hexdigest().lower()
    if (hashh != posted_hash):
        print "Invalid Transaction. Please try again"
    else:
        print "Thank You. Your order status is ", status
        print "Your Transaction ID for this transaction is ", txnid
        print "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."

    return render_to_response('sucess.html',
                              RequestContext(request, {"txnid": txnid, "status": status, "amount": amount}))


@csrf_protect
@csrf_exempt
def failure(request):
    import ipdb;ipdb.set_trace()
    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "GQs7yium"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq).hexdigest().lower()
    if (hashh != posted_hash):
        print "Invalid Transaction. Please try again"
    else:
        print "Thank You. Your order status is ", status
        print "Your Transaction ID for this transaction is ", txnid
        print "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."
    return render_to_response("Failure.html", RequestContext(request, c))
