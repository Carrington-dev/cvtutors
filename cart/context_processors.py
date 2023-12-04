from cart.models import *
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart, CartItem
from cart.views import _cart_id
from pay.utils import convert_now
# Create your views here.


def show_me(request):
    total=0
    quantity=0
    cart_items=None
    context = {}
    total_cart_items = 0
    value_added_tax = 0
    grand_total = 0
    shipping_fee = 0
    grand_total_no_shipping = 0

    if 'admin' in request.path:
        return context
    else:
        try:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            uni = CartItem.objects.filter(cart=cart, is_active=True).count()
            
            for cart_item in cart_items:
                if cart_item.product == None:

                    total += (cart_item.course.price * cart_item.quantity )
                else:
                    total += (cart_item.product.price * cart_item.quantity )

                quantity += cart_item.quantity
                total_cart_items += ( cart_item.quantity )

            a = (float(15/100) * float(total))
            value_added_tax = round(a,2)
            grand_total_no_shipping = round((float(115/100) * float(total)),2 )

            # total = total + int(value_added_tax)

            if grand_total_no_shipping > 1400:
                shipping_fee = 0.00
            
            grand_total =  float(grand_total_no_shipping) + float(shipping_fee) 

        except ObjectDoesNotExist:
            pass

    
    
    context['total'] = round(total, 2)
    # print(round(convert_now('USD', 'ZAR', round(total, 2)), 2))
    context['total_cost_in_dollars'] = round(convert_now('USD', 'ZAR', round(total, 2)), 2)

    context['value_added_tax'] = round(value_added_tax, 2)
    context['grand_total'] = round(grand_total, 2)
    context['shipping_fee'] = round(shipping_fee, 2)
    context['grand_total_no_shipping'] = round(grand_total_no_shipping, 2)
    context['quantity'] = quantity
    context['total_cart_items'] = total_cart_items
    context['cart_items'] = cart_items
    # context['order'] = order_id
    
    return context