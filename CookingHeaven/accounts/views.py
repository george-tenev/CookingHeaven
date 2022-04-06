from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from CookingHeaven.accounts.forms import UserRegisterForm, SuperUserProfileCreationForm, \
    SuperUserGroupCreateForm, ProfileUpdateForm
from CookingHeaven.accounts.models import CookingHeavenUser, Profile
from CookingHeaven.common.view_mixins import SuperuserRequiredMixin
from CookingHeaven.main.models import Recipe

UserModel = get_user_model()


class ProfileUpdateCheckCorrectUserMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.pk == self.object.pk or request.user.is_superuser:
            return response
        return redirect(reverse_lazy('home'))

class GroupCreateView(LoginRequiredMixin, SuperuserRequiredMixin, views.CreateView):
    template_name = 'admin/group_create_view.html'
    success_url = reverse_lazy('home')
    form_class = SuperUserGroupCreateForm


class SuperUserProfileCreateView(LoginRequiredMixin, SuperuserRequiredMixin, views.CreateView):
    template_name = 'admin/admin_profile_create.html'
    success_url = reverse_lazy('home')
    form_class = SuperUserProfileCreationForm


class UserRegisterView(views.CreateView):
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')


# class ProfileUpdateView(views.UpdateView):
#     template_name = 'accounts/user_update.html'
#     form_class = UserRegisterForm
#     success_url = reverse_lazy('home')
#     context_object_name = 'user'
#     model = UserModel

class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/user_login.html'


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class UserDeleteView(LoginRequiredMixin, ProfileUpdateCheckCorrectUserMixin, views.DeleteView):
    model = CookingHeavenUser
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('home')


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('dashboard')


class ProfileUpdateView(LoginRequiredMixin, ProfileUpdateCheckCorrectUserMixin, views.UpdateView):
    model = Profile
    template_name = 'accounts/profile_update.html'
    form_class = ProfileUpdateForm
    context_object_name = 'profile'

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return reverse_lazy(
            'profile details',
            kwargs={
                'pk': self.object.pk
            }
        )


class ProfileDetailsView(LoginRequiredMixin,ProfileUpdateCheckCorrectUserMixin, views.DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = Recipe.objects.filter(publisher=self.object.pk)
        context['recipes'] = recipes
        context['total_likes'] = sum(recipe.likes.count() for recipe in recipes)
        return context


class ProfileListView(views.ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'admin/profile_list.html'
