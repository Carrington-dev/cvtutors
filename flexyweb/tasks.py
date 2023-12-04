from flexyweb import settings
from celery import shared_task
from django.core.mail import send_mail
from panel.models import Order
import socket
socket.getaddrinfo('localhost', 8080)

@shared_task
def order_created(order_id):
    """Task to send an e-mail notification when an order is successfully created."""
    order = Order.objects.get(id=order_id)
    subject = f'MyTuta Order number. {order.order_number}'
    message = f'Dear {order.first_name},\n\nYou have successfully started an ordering process. Your order number is {order.order_number}.We will contact you on {order.phone}.\n\nPlease continue to pay for your items. Thank you.' 
    mail_sent = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])
    return mail_sent


def order_created_helper(order_id):
    """Task to send an e-mail notification when an order is successfully created."""
    order = Order.objects.get(id=order_id)
    subject = f'MyTuta Order number. {order.order_number}'
    message = f'Dear {order.first_name},\n\nYou have successfully started an ordering process. Your order number is {order.order_number}.We will contact you on {order.phone}.\n\nPlease continue to pay for your items. Thank you.' 
    mail_sent = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])
    return mail_sent