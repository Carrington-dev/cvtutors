from django.contrib import admin

from pay.models import Payment

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    '''Admin View for Payment'''

    list_display = ( 'payment_id', 'payment_method', 'card_number', 'amount_paid', 'status', 'created_at')
    list_filter = ('status',)
    # inlines = [
    #     Inline,
    # ]
    raw_id_fields = ('user',)
    readonly_fields = ('user', 'payment_method')
    search_fields = ('user', 'payment_id',)
    date_hierarchy = 'created_at'
    ordering = ('-pk',)