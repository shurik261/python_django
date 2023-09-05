from django.urls import path
from .views import view_func

urlpatterns = [
    path('func/', view_func, name='view_func'),

]