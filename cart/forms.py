from django.forms import ModelForm
import panel.models

class OrderForm3(ModelForm):
    class Meta:
        model = panel.models.Order
        fields = [ "payment_method"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})