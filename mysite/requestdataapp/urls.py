from django.urls import path
from .views import proces_get_view, user_form, handle_file_upload

urlpatterns = [
    path('get/', proces_get_view, name='get_view'),
    path('bio/', user_form, name='user_form'),
    path('upload/', handle_file_upload, name='file_upload'),
]