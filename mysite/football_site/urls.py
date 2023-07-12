from django.urls import path
from .views import football_index
app_name = 'football_site'
urlpatterns = [
    path('', football_index, name='index')
]