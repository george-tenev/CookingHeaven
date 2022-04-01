from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views

from CookingHeaven.accounts.models import Profile
from CookingHeaven.main.models import Recipe


class IndexTemplateView(views.TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        recipes = Recipe.objects.all()
        context['recipes'] = recipes
        return context



class DashboardView(views.ListView):
    model = Recipe
    template_name = 'main/dashboard.html'
    context_object_name = 'recipes'
    paginate_by = 3
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     recipes = Recipe.objects.all()
    #     self.object_list = recipes
    #     return context