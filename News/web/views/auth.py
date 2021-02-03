from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic.edit import CreateView

from web.forms import auth


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = auth.SignUpForm

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('landing')


class LoginView(BaseLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('landing')


class LogoutView(BaseLogoutView):
    template_name = 'logout.html'
