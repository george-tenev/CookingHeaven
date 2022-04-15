from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views

from CookingHeaven.accounts.models import Profile
from CookingHeaven.main.forms import RecipeCategoryFilterForm
from CookingHeaven.main.models import Recipe, Category


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
        filter = self.request.GET.get("filter")
        queryset = Recipe.objects.filter(category__name=filter) if filter is not None else Recipe.objects.all()
        queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DashboardView, self).get_context_data(object_list=None, **kwargs)
        filter_form = RecipeCategoryFilterForm()
        categories = {
            'filter_form': filter_form,
            'categories': Category.objects.all(),
        }
        context.update(categories)
        return context


