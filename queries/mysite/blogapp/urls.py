from django.urls import path
from .views import blog_index, BasedListView


app_name = 'blogapp'
urlpatterns = [
    path('', blog_index, name='index'),
    path('based/', BasedListView.as_view(), name='based'),
]

