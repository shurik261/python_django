from django.urls import path
from .views import proces_get_view, user_form,view_func

urlpatterns = [
    path('get/', proces_get_view, name='get_view'),
    path('bio/', user_form, name='user_form'),
    # path('upload/', handle_file_upload, name='file_upload'),
    path('func/', view_func, name='view_func'),
]