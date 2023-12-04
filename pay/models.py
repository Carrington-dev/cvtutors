from datetime import datetime
import math
import random
from secrets import choice
from django.db import models
from flexyweb import  settings

# Create your models here.
def _generate_payment_id():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890()!*$#%&^@'.lower()
    c_length = len(characters)

    OTP = ""
    for i in range(30) :
        OTP += characters[math.floor(random.random() * c_length)]
    return OTP
    
class Payment(models.Model):
    PAYMENT_METHOD = (
        ('Ozow','Ozow'),
        ('PayPal','PayPal'),
        ('PayFast','PayFast'),
        ('Braintree','Braintree'),
        ('CC','Credit Card'),
        ('DC','Debit Card'),
        ('eBucks','eBucks'),
        ('Mobicred','Mobicred'),
        ('Stripe','Stripe'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    payment_id = models.CharField(max_length=100, default=_generate_payment_id)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD, default="CC" )
    card_number = models.CharField(max_length=200, null=True, blank=True)
    
    amount_paid = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default="Unpaid")
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.payment_id

    class Meta:
        db_table = 'order_payments'
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
