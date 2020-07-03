from django.forms.models import ModelForm
from django.http import Http404
from django.urls import reverse
from django.views.generic.edit import UpdateView

from db import models


class UserUpdateForm(ModelForm):
    class Meta:
        model = models.User
        fields = [
            'first_name',
            'last_name',
            'email',
            'favorite_categories',
            'favorite_agencies'
        ]


class ProfileView(UpdateView):
    form_class = UserUpdateForm
    model = models.User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('profile')

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_authenticated:
            return user
        raise Http404()
