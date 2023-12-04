from django.shortcuts import render, redirect, get_object_or_404
from cart.forms import OrderForm3
from cart.utils import _generate_cart_id
from cart.models import *
from django.http import HttpResponseRedirect
from django.contrib import  messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from panel.models import Order

# Create your views here.
def _cart_id(request):
    if not "cart_id" in request.session:
        request.session["cart_id"] = _generate_cart_id()
    return request.session["cart_id"]



def add_cart(request, product_id):
    context = {"title":"Add cart" }
    product = Product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))   #get the cart using cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    is_cart_item_existing =  CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_existing:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'You have increased your {cart_item.product.name} plan hours by 1')
    
    else:
        # if product.stock > 0:
        cart_item = CartItem.objects.create(
            product=product,
            quantity = 1,
            cart = cart,

        )
        cart_item.save()
        messages.success(request, f'You have added 1 {cart_item.product.name} plan in your cart')
        # else:
        #     messages.warning(request, f"The product you are trying to add to your cart is out of stock to your cart.")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def add_cart_course(request, course_id):
    product = Course.objects.get(id=course_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))   #get the cart using cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    is_cart_item_existing =  CartItem.objects.filter(course=product, cart=cart).exists()
    if is_cart_item_existing:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(course=product, cart=cart)
        if cart_item.course:
            messages.error(request, f"You can't enrol into the same course multiple times!")
        else:
            cart_item.quantity += 1
            messages.success(request, f'You have increased your {cart_item.course.name} plan hours by 1')
        cart_item.save()
    
    else:
        # if product.stock > 0:
        cart_item = CartItem.objects.create(
            course=product,
            quantity = 1,
            cart = cart,

        )
        cart_item.save()
        messages.success(request, f'You have added {cart_item.quantity} {cart_item.course.name} plan in your cart')
        # else:
        #     messages.warning(request, f"The product you are trying to add to your cart is out of stock to your cart.")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)

    if cart_item.product:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.warning(request, f'You have removed {cart_item.product.name} in your cart')
        
        else:
            cart_item.delete()
            messages.success(request, f'You have successfully deleted {cart_item.product.name} in your cart')
    else:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.warning(request, f'You have removed {cart_item.course.name} in your cart')
        
        else:
            cart_item.delete()
            messages.success(request, f'You have successfully deleted {cart_item.course.name} in your cart')
    

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def increase_cart(request, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
    if cart_item.course:
        messages.error(request, f"You can't enrol into the same course multiple times!")
    else:
        cart_item.quantity += 1
        messages.success(request, f'You have added 1 {cart_item.product.name} in your cart')
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_cart_item(request, cart_item_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id = product_id)
    # cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
    cart_item = CartItem.objects.get(pk=cart_item_id)
    if cart_item.product:

        if cart_item.quantity > 1:
            cart_item.delete()
            messages.warning(request, f'You have deleted {cart_item.product.name} in your cart')
        
        else:
            cart_item.delete()
            messages.success(request, f'You have deleted {cart_item.product.name} in your cart')
    else:
        if cart_item.quantity > 1:
            cart_item.delete()
            messages.warning(request, f'You have deleted {cart_item.course.name} in your cart')
        
        else:
            cart_item.delete()
            messages.success(request, f'You have deleted {cart_item.course.name} in your cart')
    
    
    
    return redirect('cart')


@login_required(login_url='login')
def cart(request, total=0, quantity=0, cart_items=None):
    context = {"title":"Cart" }
   
    total = 0
    cart_items = 0
    quantity  = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product == None:

                total += (cart_item.course.price * cart_item.quantity )
            else:
                total += (cart_item.product.price * cart_item.quantity )
            # total += (cart_item.product.price * cart_item.quantity )
            quantity += cart_item.quantity

        

    except ObjectDoesNotExist:
        pass
    
    if quantity == 0:
        messages.warning(request, f'You can not view an empty cart.')
        return redirect("pricing")
    
    context['title'] = "Cart"
    id = request.session.get('order_id')
    if id is None:
        return redirect("apply1")
    order = Order.objects.get(id=id)    
    context["order"] = order
    # request.session['total_in_rands'] = total

    if request.method == 'POST':
        form = OrderForm3(request.POST)
        if form.is_valid():
            # form.save()
            order = get_object_or_404(Order, pk=id)
            order.payment_method = form.cleaned_data['payment_method']
            order.save()
            messages.warning(request, f'You will be redirected to pay now.')
            """Redirect now"""
            if order.payment_method == "PayFast":
                return redirect("payfast")
            if order.payment_method == "PayPal":
                return redirect("paypal")
            if order.payment_method == "Ozow":
                return redirect("ozow")
            if order.payment_method == "Yoco":
                return redirect("yoco")
            # if order.payment_method == "Yoco":
            #     return redirect("Yoco")
               
    else:
        form = OrderForm3()
    context['form'] = form
    return render(request, "cart/cart.html", context)
