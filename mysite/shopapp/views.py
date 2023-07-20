from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .models import Product, Order

def shop_index(request: HttpRequest):
    products = [
        ('Bmw', 15000),
        ('Toyota', 10000),
        ('Жигули', 2000),
    ]
    auto = [
        {'name': 'Bmw','price': 15000, 'currency': '€', 'country': 'Германия'},
        {'name': 'Toyota', 'price': 10000, 'currency': '$','country': 'Япония'},
        {'name': 'Жигули', 'price': 2000000, 'currency': '₽','country': 'Россия'},
        {'name': 'Honda', 'price': 9000, 'currency': '$', 'country': 'Япония'},
    ]
    context = {
        'time_running': default_timer,
        'products': products,
        'auto': auto
    }
    return render(request, 'shopapp/shop-index.html', context=context)

def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)
def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)

def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all(),
    }
    return render(request, 'shopapp/order-list.html', context=context)

