from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    logout_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    UserListView,
    UserProfileDetailView,
    HelloView,
)

app_name = 'myauth'
urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='myauth/login.html',
             redirect_authenticated_user=True,
         ),
         name='login'),
    # path('logout/', logout_view, name='logout'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_profile/<str:username>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('register/', RegisterView.as_view(), name='register'),

    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),

    path('session/get/', get_session_view, name='session-get'),
    path('session/set/', set_session_view, name='session-set'),
    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),

]