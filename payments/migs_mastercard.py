from django.conf import settings
import hashlib
import urllib


class MigsClient(object):
    def __init__(self):
        self.secure_secret = settings.MASTERCARD_SECURE_HASH
        self.vpcURL = settings.VPC_URL
        self.payload = {}

    def hash_all_fields(self, fields):
        buf = ""
        # create a list and sort it
        fieldNames = fields.keys()
        fieldNames.sort()
        # create a buffer for the md5 input and add the secure secret first
        buf = buf + self.secure_secret
        for key in fieldNames:
            print key, fields[key]
            buf = buf + fields[key]
            # iterate through the list and add the remaining field values
        # create the md5 hash and UTF-8 encode it
        try:
            m = hashlib.md5()
            m.update(buf)
            ba = m.hexdigest()
            ba = ba.upper()
            return ba

        except Exception, e:
            import traceback
            traceback.print_exc()

    def setup(self, fields, additional_fields=None):
        # The Page does a redirect to the Virtual Payment Client
        # retrieve all the parameters into a hash map
        # no need to send the vpc url, EnableAVSdata and submit button to the vpc

        '''
        Retrieve the order page URL from the incoming order page and add it to 
        the hash map. This is only here to give the user the easy ability to go 
        back to the Order page. This would not be required in a production system
        NB. Other merchant application fields can be added in the same manner
        '''

        '''
        Create MD5 secure hash and insert it into the hash map if it was created
        created. Remember if self.secure_secret = "" it will not be created
        '''
        if self.secure_secret:
            secureHash = self.hash_all_fields(fields)
            fields["vpc_SecureHash"] = secureHash

        # Create a redirection URL
        buf = self.vpcURL + '?'
        if not additional_fields:
            buf = buf + urllib.urlencode(fields)
        else:
            buf = buf + urllib.urlencode(fields) + "&" + urllib.urlencode(additional_fields)
        return buf
        # return fields["vpc_ReturnURL"], buf

    def post_setup(self, fields, additional_fields=None):

        try:
            if self.secure_secret:
                secureHash = self.hash_all_fields(fields)
                fields["vpc_SecureHash"] = secureHash

            return self.vpcURL, fields
        except:
            import traceback
            traceback.print_exc()

    def generate_payload(self):
        return {'Title': settings.VPC_TITLE, 'vpc_AccessCode': settings.VPC_ACCESSCODE,
                   'vpc_Amount': '100', 'vpc_Command': settings.VPC_COMMAND, 'vpc_Locale': 'en',
                   'vpc_MerchTxnRef': 'ORDER958743-1', 'vpc_Merchant': settings.VPC_MERCHANT,
                   'vpc_OrderInfo': 'VPC Example', 'vpc_ReturnURL': settings.VPC_RETURN_URL,
                   'vpc_Version': settings.VPC_VERSION
               }

    def generate_get_url(self):
        payload = self.generate_payload()
        return self.setup(payload)
