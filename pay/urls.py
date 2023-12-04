from django.urls import path
from . import views as cart_views

urlpatterns = [
    path("payment/", cart_views.payment, name='yocoy'),
    path("yoco/", cart_views.payment_yoco, name='yoco_payment'),
    path("payfast/", cart_views.payfast, name='payfast'),
    path("mcard/", cart_views.paycard, name='mastercard'),
    path("yoco/", cart_views.yoco, name='yoco'),
    path("ozow/", cart_views.payozow, name='ozow'),
    path("paypal/", cart_views.paypal, name='paypal'),
    path("processing/", cart_views.pay_clear, name='ppaypal'),
    # path('paypal-payment-process/', cart_views.payment_processing, name='yoco'),
    path('before/', cart_views.pay_before, name='before'),
    path('done/', cart_views.payment_done, name='done'),
    path('canceled/', cart_views.payment_canceled, name='canceled'),
    path('notify/', cart_views.payfast_pay_clear, name='notify'),

    path('order/<int:pk>/', cart_views.OrderDetailView.as_view(), name="my_customer_order"),
    path('orders/', cart_views.my_orders, name="my_customer_orders"),
    # path('order/inv-no/<int:order_id>/', cart_views.admin_order_detail, name='admin_order_detail'),
    path('reciept/<int:order_id>', cart_views.invoice_order_detail, name='admin_order_detail'),
]