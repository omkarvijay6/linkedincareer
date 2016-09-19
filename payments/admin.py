from django.contrib import admin

# Register your models here.
from payments.models import Order, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('batch_scheduled_date', 'status', 'status_message', 'transaction_num',
                    'card_type', 'receipt_no', 'order', 'updated_ts', 'created_ts',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'merch_txn_ref', 'amount', 'country', 'updated_ts', 'created_ts')
