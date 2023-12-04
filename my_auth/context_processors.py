from decouple import config
from my_auth.countries import cities


def show_countries(request):
    context = {}
    context['cities'] = cities    
    context['company'] = "Carrington Visionary Academy"    
    context['payfast_merchant_id'] = config("payfast_merchant_id")
    context['payfast_merchant_key'] = config("payfast_merchant_key")   
    context['action'] = 'https://sandbox.payfast.co.za​/eng/process'   
    # context['company'] = "FlexyTuta"    
    # print(f"payfast_merchant_id {type(config('payfast_merchant_id'))}")
    return context