from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views

from CookingHeaven.accounts.models import Profile
from CookingHeaven.main.models import Recipe


class IndexTemplateView(views.ListView):
    model = Recipe
    template_name = 'main/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.order_by('-created_at')[:3]
        return queryset


class DashboardView(views.ListView):
    model = Recipe
    template_name = 'main/dashboard.html'
    context_object_name = 'recipes'
    paginate_by = 3

    def get_queryset(self):
        queryset = Recipe.objects.order_by('-created_at')
        return queryset

