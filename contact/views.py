# from email.message import EmailMessage
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from contact.forms import ContactForm, SubscribeForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from contact.models import Contact, Subscribe
from contact.serializers import ContactSerializer
from rest_framework.response import Response
from rest_framework import status
from flexyweb import settings
from django.template.loader import render_to_string, get_template
# Create your views here.

# from learn.models import Module

# # Create your views here.
# a = Module.objects.get(id=1)
# for i in range(12):
#     Module.objects.create(
#         title=a.title,
#         # 'course', 'title', 'description', 'order'
#         course=a.course,
#         description=a.description,
#         order=i+2,
#     )

class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer

    def get(self, request):
        contact = Contact.objects.all()
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)
    
    # def post(self, request, id=None):
    #     contact = Contact.objects.get(id=id)
    #     serializer = ContactSerializer(contact)
    #     return Response(serializer.data)
    
    
    def retrive(self, request, pk=None):
        contact = get_object_or_404(self.queryset, pk=pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    def delete(self):
        contact = self.get_object()
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Contact.objects.all()
    

# Create your views here.
def contact(request):
    context = {
        "title":"Contact | Private Home Tutors"
    }
   
    if request.method == 'POST':
        
        form = ContactForm(request.POST)
       
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            form.save()
            messages.success(request, 'Your information has been submitted')
            # return redirect('account:form_submitted')
            subject = "MyTuta Platform"
            to = ['crn96m@gmail.com']
            from_email = settings.DEFAULT_FROM_EMAIL
            contact_link = request.scheme + "://" + request.META['HTTP_HOST'] + "/admin"
            w_link = request.scheme + "://" + request.META['HTTP_HOST']
            # print(contact_link)

            ctx = {
                'c_link':contact_link,
                'w_link':w_link,
                'email': email, 
                'subject': subject, 
                'name': name, 
                'message': message, 
            }

            message = get_template('email/contact_email.html').render(ctx)
            # message = get_template('all/email.html').render(Context(ctx))
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            return redirect('contact')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            # messages.error(request, "Your information was not submitted!.")
        
   
    else:
        form = ContactForm()
    context["form"] = form
    return render(request, "contact/contact.html", context)

def subcribe(request):
    context = {"title":"Subscribe" }
    form = SubscribeForm()
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            p = form.save()
            messages.success(request, "You have successfully subscribed to our newsletters!.")
            return redirect("home")
        else:
            messages.error(request, "Email address already taken, please use a different one!.")
            

    context['form'] = form
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    