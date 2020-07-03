from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.shortcuts import reverse, render
from django.views import View
from django.views.generic.edit import CreateView

from web.forms import auth


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = auth.SignUpForm

    def get_success_url(self):
        return reverse('signup_success')


class SignUpSuccessView(View):

    def get(self, request):
        return render(request, template_name='signup_success.html')


class LoginView(BaseLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('login-success')


class LoginSuccessView(View):
    def get(self, request):
        return render(request, template_name='login_success.html')


class LogoutView(BaseLogoutView):
    template_name = 'logout.html'
