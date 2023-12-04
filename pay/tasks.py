from flexyweb import settings
from panel.models import Order
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template


def payment_completed(order_id):
    """Task to send an e-mail notification when an order is successfully created."""
    order = Order.objects.get(id=order_id)

    email = order.email
    subject = "Successful Order"
    name = order.first_name + " " + order.last_name
   
    subject = "MyTuta Platform"
    to = ['crn96m@gmail.com']
    from_email = settings.DEFAULT_FROM_EMAIL
    # contact_link = request.scheme + "://" + request.META['HTTP_HOST'] + "/admin"
    # w_link = request.scheme + "://" + request.META['HTTP_HOST']
    # print(contact_link)

    ctx = {
        # 'c_link':contact_link,
        # 'w_link':w_link,
        'email': email, 
        'subject': subject, 
        'name': name, 
        'order': order, 
        # 'message': message, 
    }

    message = get_template('payment/do_ne.html').render(ctx)
    # message = get_template('all/email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    return msg