import jwt
from datetime import datetime

def generate_unique_merch_txn_ref():
    unique_no = datetime.now().strftime(("%f%d%m%Y%S%M%H"))
    unique_order_id = jwt.encode({}, unique_no, algorithm='HS256')[-20:].upper
    return "ORDER" + "-" + unique_order_id
