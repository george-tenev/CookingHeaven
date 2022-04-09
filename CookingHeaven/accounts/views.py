from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic import DeleteView

from CookingHeaven.accounts.forms import UserRegisterForm, SuperUserProfileCreationForm, \
    SuperUserGroupCreateForm, ProfileUpdateForm, UserUpdateForm
from CookingHeaven.accounts.models import CookingHeavenUser, Profile
from CookingHeaven.common.view_mixins import SuperuserRequiredMixin, AdminRequiredMixin
from CookingHeaven.main.models import Recipe

UserModel = get_user_model()


class ProfileCheckCorrectUserMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.pk == self.object.pk or request.user.is_superuser:
            return response
        raise PermissionError

class Success_Url_ProfileDetailsViewMixin:
    def get_success_url(self):
        return reverse(
            'profile details',
            kwargs={
                'pk': self.object.pk
            }
        )

class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, views.CreateView):
    template_name = 'admin/group_create.html'
    success_url = reverse_lazy('home')
    form_class = SuperUserGroupCreateForm
    permission_required = 'auth.add_group'


class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, views.UpdateView):
    model = Group
    template_name = 'admin/group_update.html'
    success_url = reverse_lazy('home')
    form_class = SuperUserGroupCreateForm
    permission_required = 'auth.change_group'
    context_object_name = 'group'


class GroupDeleteView(LoginRequiredMixin, AdminRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.delete_group'


class GroupListView(PermissionRequiredMixin, views.ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'admin/group_list.html'
    permission_required = 'auth.view_group'


class SuperUserProfileCreateView(LoginRequiredMixin, SuperuserRequiredMixin, views.CreateView):
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


class UserDeleteView(LoginRequiredMixin, ProfileCheckCorrectUserMixin, views.DeleteView):
    model = CookingHeavenUser
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('home')


class ProfileUpdateView(LoginRequiredMixin, ProfileCheckCorrectUserMixin,Success_Url_ProfileDetailsViewMixin, views.UpdateView):
    model = Profile
    template_name = 'accounts/profile_update.html'
    form_class = ProfileUpdateForm
    context_object_name = 'profile'


class ProfileDetailsView(LoginRequiredMixin, ProfileCheckCorrectUserMixin, views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = list(Recipe.objects.filter(publisher=self.object.pk))
        context['recipes'] = recipes
        context['total_likes'] = sum(recipe.likes.count() for recipe in recipes)
        return context


class AdminUserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, Success_Url_ProfileDetailsViewMixin, views.UpdateView):
    model = UserModel
    template_name = 'accounts/user_update.html'
    form_class = UserUpdateForm
    context_object_name = 'user'
    permission_required = 'accounts.change_cookingheavenuser'


class ProfileListView(PermissionRequiredMixin, views.ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'admin/profile_list.html'
    permission_required = 'accounts.view_cookingheavenuser'


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('dashboard')
