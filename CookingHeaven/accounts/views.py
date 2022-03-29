from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from CookingHeaven.accounts.forms import UserRegisterForm, SuperUserProfileCreationForm
from CookingHeaven.accounts.models import CookingHeavenUser, Profile
from CookingHeaven.common.view_mixins import SuperuserRequiredMixin

UserModel = get_user_model()


# TODO Restrict access to views via UserPassesTestMixin


class AdminCreateProfileView(LoginRequiredMixin, SuperuserRequiredMixin, views.CreateView):
    template_name = 'admin/admin_profile_create.html'
    success_url = reverse_lazy('home')
    form_class = SuperUserProfileCreationForm


class UserRegisterView(views.CreateView):
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/user_login.html'


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class UserDeleteView(LoginRequiredMixin, views.DeleteView):
    model = CookingHeavenUser
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('home')


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('dashboard')


class ProfileUpdateView(LoginRequiredMixin, views.UpdateView):
    model = CookingHeavenUser
    template_name = 'accounts/profile_update.html'


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
        # TODO get recipes, recipes count, likes