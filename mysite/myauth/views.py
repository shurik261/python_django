from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import AvatarUpdateForm
from .models import Profile
from django.views import View

class AboutMeView(View):
    template_name = 'myauth/about-me.html'

    def get(self, request, *args, **kwargs):
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        form = AvatarUpdateForm(instance=user_profile)
        return render(request, self.template_name, {'user_profile': user_profile, 'form': form})

    def post(self, request, *args, **kwargs):
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        form = AvatarUpdateForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')

        return render(request, self.template_name, {'user_profile': user_profile, 'form': form})

class UserListView(View):
    template_name = 'myauth/user_list.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, self.template_name, {'users': users})

class UserProfileView(View):
    template_name = 'myauth/user_profile.html'

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        try:
            user_profile = user.profile
        except Profile.DoesNotExist:
            user_profile = None

        return render(request, self.template_name, {'user_profile': user_profile})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(self.request, user=user)
        return response
def login_view(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    return render(request, 'myauth/login.html', {'error':'invalid login'})

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse('myauth:login'))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


@user_passes_test(lambda u:u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value ')
    return HttpResponse(f'Cookie value: {value!r}')

@permission_required('myauth:view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set')

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default value')
    return HttpResponse(f'Session value: {value!r}')

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})