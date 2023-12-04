from django.contrib import admin
from cart.models import Cart, CartItem
# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    '''Admin View for Cart'''

    list_display = ('cart_id', 'date_added', 'items',)
    list_filter = ('cart_id', 'date_added')
    ordering = ('-date_added',)

    def items(self, obj):
        return obj.item_count


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    '''Admin View for CartItem'''

    list_display = ('product', 'cart', 'quantity','sub_total', 'is_active')
    list_filter = ('product', 'cart', 'quantity', 'is_active')
    ordering = ('-pk',)