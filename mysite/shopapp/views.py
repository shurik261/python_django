from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

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
