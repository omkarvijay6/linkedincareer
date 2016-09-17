from payments.enums import CardTypes

CREDIT_CARD_TYPES = (
    (CardTypes.american_express_card.value, 'American Express'),
    (CardTypes.american_express_purchase_card.value, 'American Express Corporate Purchase Card'),
    (CardTypes.diners_club_card.value, 'Diners Club'),
    (CardTypes.gap_inc_card.value, 'GAP Inc. card'),
    (CardTypes.generic_card.value, 'Generic Card'),
    (CardTypes.jcb_card.value, 'JCB Card'),
    (CardTypes.loyalty_card.value, 'Loyalty Card'),
    (CardTypes.maestro_card.value, 'Maestro Card'),
    (CardTypes.master_card.value, 'MasterCard'),
    (CardTypes.mondex_card.value, 'Mondex Card'),
    (CardTypes.plc_card.value, 'PLC Card'),
    (CardTypes.safe_debit_card.value, 'SafeDebit Card'),
    (CardTypes.solo_card.value, 'SOLO Card'),
    (CardTypes.style_card.value, 'STYLE Card'),
    (CardTypes.switch_card.value, 'SWITCH Card'),
    (CardTypes.visa_debit_card.value, 'Visa Debit Card'),
    (CardTypes.visa_card.value, 'Visa Card'),
    (CardTypes.visa_corporate_purchase_card.value, 'Visa Corporate Purchase Card'),
    (CardTypes.electronic_benifit_card.value, 'Electronic Benifit Card'),
)
