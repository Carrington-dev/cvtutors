import json
import datetime
import requests
import weasyprint
from cart.models import *
from cart.forms import OrderForm3
from django.shortcuts import render
from django.contrib import  messages
from cart.utils import _generate_cart_id
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import  DetailView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pay.tasks import payment_completed
from .utils import convert_now


# from forex_python.converter import CurrencyRates
from django.template.loader import render_to_string
# from pay.tasks import payment_completed, order_failed
from django.contrib.admin.views.decorators import staff_member_required
# from django.conf import settings

# c = CurrencyRates()
# cs = c.get_rates('USD') 

from flexyweb import settings
from pay.models import Payment
from cart.views import _cart_id
from django.http import JsonResponse
from panel.models import Order, OrderProduct
# Create your views here.

def payment(request):
    context = {"title":"Payment" }
    return render(request, "payment/yoco.html", context)

def yoco(request):
    context = {"title":"Payment" }
    return render(request, "payment/yoco.html", context)

def payment_yoco(request):
    data_body = json.loads(request.body)
    # print(data_body)
    # print(data_body)

    # Anonymous test key. Replace with your key.

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.order_total
    context = {}
    context['total_cost'] = total_cost

    # data = pay_clear(request, order, total_cost)



    

    SECRET_KEY = 'sk_test_35427c4aM1pJYkP9c094e12b38fa'
    t = total_cost*100
    response = requests.post(
    'https://online.yoco.com/v1/charges/',
    headers={
        'X-Auth-Secret-Key': SECRET_KEY,
    },
    json={
        'token': data_body['tokens'],
        'amountInCents': int(t),
        'currency': 'ZAR',
    },
    )
    print(response.status_code)
    con = {"message":"Payment not successful try again",}
   
    # response.status_code will contain the HTTP status code
    # response.json() will contain the response body
    return JsonResponse(con, safe=False)

def payfast(request):
    context = {"title":"Pay with Payfast" }
    context['title'] = "Cart"
    id = request.session.get('order_id')
    order = Order.objects.get(id=id)    
    if order.is_ordered:
        return redirect("done")
    context["order"] = order
    return render(request, "payment/payfast.html", context)

def paypal(request):
    context = {}
    context['title'] = "Cart"
    id = request.session.get('order_id')
    order = Order.objects.get(id=id)    
    if order.is_ordered:
        return redirect("done")
    context["order"] = order
    return render(request, "payment/paypal.html", context)

def payozow(request):
    context = {"title":"Payment" }
    return render(request, "payment/ozow.html", context)

def paycard(request):
    context = {"title":"Payment" }
    return render(request, "payment/mastercard.html", context)


@login_required(login_url='login')
def payment_done(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        

        cart_items.delete()
    except:
        pass
    context = {"title":"Done" }
    try:
        # request.session.pop('order_id') == None
        order_id = request.session.pop('order_id')
        order = get_object_or_404(Order, id=order_id)
        # payment_completed(order.id)
        total_cost = order.order_total
        context['total_cost'] = total_cost
        context['total_cost_in_dollars'] = convert_now('USD', 'ZAR', total_cost)
        context['order'] = order
        # delete request.session

        now = datetime.datetime.now()    
    except:
        return redirect("my_customer_orders")
    
    return render(request, 'payment/done.html', context)

@login_required(login_url='login')
def payment_canceled(request):
    context = {"title":"Payment failed" }
    return render(request, 'payment/canceled.html', context)


# def pay_clear(request, order, total_cost):
@login_required(login_url='login')
def pay_clear(request):
    id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=id)
    data_body = json.loads(request.body)
    payment = Payment(
        user = request.user,
        payment_id = data_body['transactionID'],
        payment_method = data_body['payment_method'],
        # card_number = ,
        amount_paid = data_body['total'],
        status = data_body['status'],
    )
    
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.status = "New"
    order.user = request.user
    order.order_total_other = payment.amount_paid
    order.order_total = order.get_order_total()
    order.currency = 'USD'
    order.device_name = request.headers['User-Agent']
    order.save()
    data = dict()

    """TRANSFERING CART ITEMS TO ORDER ITEMS"""

    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    # cart_items = []
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            """Cart Items"""
            order_product = OrderProduct()

            order_product.order  = order
            order_product.payment = payment
            if cart_item.product:
                order_product.product = cart_item.product
            else:
                order_product.course = cart_item.course
                order_product.course.students_enrolled.add(request.user)
            order_product.user = request.user
            order_product.quantity = cart_item.quantity
            order_product.is_ordered = True


            order_product.save()

            
            

            product = Product.objects.get(id=cart_item.product_id)
            # product.stock -= cart_item.quantity
            product.save()
        
        cart_items.delete()
        # payment_completed.delay(order.id)
        # payment_completed(order.id)
        # print("""PASSED THE @TASK METHOD HEARDING TO THE MESSAGE""")
        messages.success(request, f'You have successfully paid for your order with order number {order.order_number}')
        order.order_total = order.get_order_total()
        order.save()

        data = {
            "message": f"You have successfully paid for your order with order number {order.order_number}",
            "order_number": order.order_number,
            "transID": payment.payment_id,
        }
    except ObjectDoesNotExist:
        pass
    if cart_items:
        cart_items.delete()
    return JsonResponse(data, safe=True)
# def pay_clear(request, order, total_cost):
@login_required(login_url='login')
def pay_before(request):
    id = request.session.get('order_id')
    order = get_object_or_404(Order, pk=id)
    # data_body = json.loads(request.body)
    payment = Payment(
        user = request.user,
        payment_id = order.order_number,
        payment_method = "PayFast",
        amount_paid = order.get_order_total(),
        status = "COMPLETED",
    )
    
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.status = "New"
    order.user = request.user
    order.order_total_other = payment.amount_paid
    order.order_total = order.get_order_total()
    order.currency = 'ZAR'
    order.device_name = request.headers['User-Agent']
    order.save()
    data = dict()

    """TRANSFERING CART ITEMS TO ORDER ITEMS"""

    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    # cart_items = []
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            """Cart Items"""
            order_product = OrderProduct()

            order_product.order  = order
            order_product.payment = payment
            if cart_item.product:
                order_product.product = cart_item.product
            else:
                order_product.course = cart_item.course
                order_product.course.students_enrolled.add(request.user)
            order_product.user = request.user
            order_product.quantity = cart_item.quantity
            order_product.is_ordered = True


            order_product.save()

            
            

            product = Product.objects.get(id=cart_item.product_id)
            # product.stock -= cart_item.quantity
            product.save()
        
        cart_items.delete()
        # payment_completed.delay(order.id)
        # payment_completed(order.id)
        # print("""PASSED THE @TASK METHOD HEARDING TO THE MESSAGE""")
        messages.success(request, f'You have successfully paid for your order with order number {order.order_number}')
        order.order_total = order.get_order_total()
        payment.amount_paid = order.get_order_total()
        payment.save()
        order.save()

        data = {
            "message": f"You have successfully paid for your order with order number {order.order_number}",
            "order_number": order.order_number,
            "transID": payment.payment_id,
        }
    except ObjectDoesNotExist:
        pass
    if cart_items:
        cart_items.delete()
    return redirect("done")

@login_required(login_url='login')
def payfast_pay_clear(request):
    data_body = json.loads(request.body)
    data = dict()
    print(data_body)
    return JsonResponse(data, safe=True)

class OrderDetailView(DetailView):
    model = Order
    template_name='orders/order_detail.html'
    context_object_name = 'order'
    

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
       
        context['title'] = "Order " + str(self.object.order_number)
        return context



@login_required(login_url='login')
def my_orders(request):
    context = {"title":"All orders" }
    if request.method == 'POST':
        orderss = request.POST.get('orders')
        orders = Order.objects.all().order_by("-pk").filter(order_number__startswith=orderss).values()
        orders = orders.filter(user=request.user)
    else:
        orders = Order.objects.all().order_by("-pk")
        orders = orders.filter(user=request.user)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 20)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context['orders'] = orders
    # context['orders'] = orders.filter(user=request.user)
    context['title'] = "Orders"
    return render(request, 'orders/order_list.html', context)



# @staff_member_required
def invoice_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    image = settings.STATIC_ROOT + "images/logo.png"
    html = render_to_string('orders/order/invoice.html', {'order': order, 'image':image})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={order.order_number}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response,
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/template.css')])
    return response