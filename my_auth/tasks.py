import socket
from time import sleep
from django import template
from flexyweb import settings
from celery import shared_task
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator

socket.getaddrinfo('localhost', 8080)



# 
# @shared_task
def send_verification_email(request, user):
    sleep(10)
    """Task to send an e-mail notification when an order is successfully created."""
    # """
    subject = "Verify your account"
    plaintext = template.loader.get_template('registration/password_reset_email.txt')
    htmltemp = template.loader.get_template('email/confirm_real.html')
    # htmltemp = template.loader.get_template('registration/password_reset_email.html')
    c = { 
    "email":user.email,
    'domain':request.META['HTTP_HOST'],
    'site_name': 'FlexyTuta',
    "uid": urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
    "user": user,
    'token': default_token_generator.make_token(user),
    'protocol': request.scheme,
    'web_link':  request.scheme + "://" + request.META['HTTP_HOST'] + "/"
    }
    text_content = plaintext.render(c)
    html_content = htmltemp.render(c)
    try:
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email], headers = {'Reply-To': f'{user.email}'})
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return 
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    # """
    return
