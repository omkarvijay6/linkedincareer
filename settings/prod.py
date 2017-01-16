from settings.base import *
DEBUG = False

PAYPAL_TEST = False
ALLOWED_HOSTS = ['*']

# not required as it is handled by nginx
# SECURE_SSL_REDIRECT = True # [1]
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')