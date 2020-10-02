from django.shortcuts import render
from django.db import models

from app.models import Order, Payment

# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')


def orders(request):
    order = Order.objects.all().order_by('-ordered_date')
    return render(request, 'dashboard/orders.html', {'order': order})

