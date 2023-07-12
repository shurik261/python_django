from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

def football_index(request: HttpRequest):
    tabl = [
        {'number': 1, 'team': 'Real M'}
    ]
    context = {
        'time_running': default_timer
    }
    return render(request, 'football_site/football-index.html', context=context)
