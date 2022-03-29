from django.urls import reverse_lazy
from django.views import generic as views

from CookingHeaven.main.forms import IngredientCreateForm
from CookingHeaven.main.models import Ingredient


class IngredientCreateView(views.CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = 'partials/ingredient_form.html'
    success_url = reverse_lazy('ingredient create form')

