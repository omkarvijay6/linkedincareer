import hashlib
from django.core.urlresolvers import reverse

def generate_payumoney_post_data(user, service, transaction_id):
    key = "rjQUPktU"
    SALT = "e5iIg1jwi8"
    PAYU_BASE_URL = "https://test.payu.in/_payment"
    optional_posted = {'city': '', 'zipcode': '', 'state': '',  'firstname': 'vijay', 'address1': '', 'address2': '',
                       'lastname': '', 'udf1': '', 'udf3': '', 'udf2': '', 'udf5': '', 'udf4': '', 'country': '',
                       'curl': '', 'pg': ''}
    success_url = 'http://localhost:8000' + reverse('payumoney_success')
    failure_url = 'http://localhost:8000' + reverse('payumoney_failure')
    posted = {'key': key, 'txnid': transaction_id, 'amount': '100', 'productinfo': 'skdjfk', 'firstname': 'vijay',
              'email': 'omkarvijay5@gmail.com', 'phone': '9010669836', 'surl': success_url,
              'furl': failure_url, 'service_provider': 'payu_paisa'
              }
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
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
    posted['hash'] = hashh
    posted['hash_string'] = hash_string
    return posted, PAYU_BASE_URL
