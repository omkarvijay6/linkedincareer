from settings.base import *
DEBUG = False

PAYPAL_TEST = False

SECURE_SSL_REDIRECT = True # [1]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')