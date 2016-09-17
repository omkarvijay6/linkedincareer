from enum import Enum

class CardTypes(Enum):
    american_express_card = 'AE'
    american_express_purchase_card = 'AP'
    diners_club_card = 'DC'
    gap_inc_card = 'GC'
    generic_card = 'XX'
    jcb_card = 'JC'
    loyalty_card = 'LY'
    maestro_card = 'MS'
    master_card = 'MC'
    mondex_card = 'MX'
    plc_card = 'PL'
    safe_debit_card = 'SD'
    solo_card = 'SO'
    style_card = 'ST'
    switch_card = 'SW'
    visa_debit_card = 'VD'
    visa_card = 'VC'
    visa_corporate_purchase_card = 'VP'
    electronic_benifit_card = 'EB'

class StatusChoices(Enum):

    successful = '0'
    pending = '1'
    failed = '2'
