from django import forms
from django.forms import ModelForm
from contact.models import *

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'subject', 'message')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter your full name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Enter your message', 'type':'text'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Enter your phone'})
        self.fields['subject'].widget.attrs.update({'placeholder': 'Enter your subject'})
		
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = ('email',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})