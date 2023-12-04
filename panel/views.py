import json
from webbrowser import get
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from flexyweb.tasks import order_created, order_created_helper
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib import messages
from panel.forms import *
from django.contrib import messages
import datetime
from my_auth.countries import cities
from panel.models import Product
from panel.serializers import PostSerializer
from panel.utils import order_generate_number

# Create your views here.
def apply1(request):
    message = None
    form  = OrderForm1()
    if request.method == 'POST':
        form = OrderForm1(request.POST)
        if form.is_valid():
            p = form.save()
            order_num = order_generate_number(p.id)
            data = get_object_or_404(Order, pk=p.id)
            data.order_number = order_num
            data.save()
            request.session['order_id'] = data.id
                # order_created.delay
            order_created.delay(data.id)

            message = "Infomartion was submitted successfully"
            messages.add_message(request, messages.INFO, message)
            return redirect("apply2")
           
    else:
        pass
        # form = OrderForm1()

    return render(request, "apply/apply1.html", {'form':form, 'title':"Ordering process"})

def apply2(request):
    message = None
    
    if request.method == 'POST':
        form = OrderForm2(request.POST)
        if form.is_valid():
            id = request.session.get('order_id')
            data = get_object_or_404(Order, pk=id)
            data.type_of_class = form.cleaned_data["type_of_class"]
            data.city = form.cleaned_data["city"]
            data.street_name = form.cleaned_data["street_name"]
            data.zip_code = form.cleaned_data["zip_code"]
            data.save()
            message = "Infomartion was submitted successfully"
            messages.add_message(request, messages.INFO, message)
            order_created.delay(id)
            # order_created_helper(id)
            return redirect("apply3")
    else:
       
        form = OrderForm2()
    return render(request, "apply/apply2.html", {"form":form, 'title':"Master Maths Tutoring Company"})

def apply3(request):
    id = request.session.get('order_id')
    if id is None:
        return redirect("apply1")
    
    order = Order.objects.get(id=id)
    if order.status != 'Started':
        return redirect("apply1")
    order_number = order.order_number
    products = Product.objects.filter(status='published')
    # products = Product.objects.all()
    context = {'products':products, "order_number":order_number, 'title':"Master Maths Tutoring Company"}
    context["order"] = order
    # order_id = request.session.get('order_id')
    return render(request, "apply/apply3.html", context)

def pricing(request):
    courses = Product.objects.filter(status='published')
    context = dict()
    context["products"] = courses
    context['title'] = "Master Maths Tutoring Company Prices"
    return render(request, "apply/pricing.html", context)

def cities_json(request):
    data = json.dumps(cities),
    # return JsonResponse(data, safe=False)
    return HttpResponse(data)
    # return data

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        serializer = PostSerializer(self.queryset)
        return Response(serializer.data)
