"""
Views for user creation, deletion, viewing.
"""


from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from lazysignup.utils import is_lazy_user

from core.models import Paste
from core.lazysignup import convert
from web.views import ListPastes


__all__ = ['LoginView', 'Register', 'Profile', 'ListMyPastes']


class LoginView(auth_views.LoginView):
    """Log in page.

    Contains a link to the Register page."""

    def form_valid(self, form):
        convert(self.request.user, form.get_user())
        return super().form_valid(form)


class Register(generic.CreateView):
    """Register a new user."""

    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/register.html'

    # Via https://stackoverflow.com/questions/3222549/
    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        convert(self.request.user, new_user)
        login(self.request, new_user)
        return response


class Profile(ListPastes):
    """View profile of any user."""

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only allow others to view profiles of "registered" of regular users,
        # but allow automatically created (session) users to view their own
        # profile.
        if is_lazy_user(self.user) and self.user != self.request.user:
            raise Http404()
        context['user'] = self.user
        return context

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return Paste.objects.filter(author__username=self.user).order_by(
            self.get_ordering()
        )


class ListMyPastes(LoginRequiredMixin, generic.RedirectView):
    """List my own pastes.

    Works with lazy users."""

    pattern_name = 'profile'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['username'] = self.request.user.username
        return super().get_redirect_url(*args, **kwargs)
