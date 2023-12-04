from django.forms import ModelForm
from panel.models import Course, Order
from django import forms


class OrderForm1(ModelForm):
    class Meta:
        model = Order
        fields = ["email", "first_name", "last_name", "country", "phone", "learning_method"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Enter your phone'})
        self.fields['country'].widget.attrs.update({'placeholder': 'Enter your country', 'id':'country_id'})
        # self.fields['learning_method'].widget.attrs.update({'placeholder': 'What do you want to be tutored on?'})
		
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class OrderForm2(ModelForm):
    class Meta:
        model = Order
        fields = ["type_of_class", "city" , "street_name", "zip_code"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_of_class'].widget.attrs.update({'placeholder': 'What do you want to be tutored on?', 'id':'subject'})
        self.fields['city'].widget.attrs.update({'placeholder': 'Enter your city name', 'id':'city_in'})
        self.fields['street_name'].widget.attrs.update({'placeholder': 'Enter your street name'})
        self.fields['zip_code'].widget.attrs.update({'placeholder': 'Enter your zip code'})
		
		# self.fields['comment'].widget.attrs.update(size='40')
        for field in self.fields:
            # name = field.name
            # name = str(name)
            self.fields[field].widget.attrs.update({'class': 'form-control'})
