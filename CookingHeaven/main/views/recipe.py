from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from CookingHeaven.main.forms import IngredientFormset, RecipeStepFormset, RecipeCreateUpdateForm
from CookingHeaven.main.models import Recipe, Ingredient, RecipeStep, FoodType


class CheckCorrectUserMixin:
    def dispatch(self, request, *args, **kwargs):
        data = super().dispatch(request, *args, **kwargs)
        if request.user != self.object.publisher:
            return redirect(reverse_lazy('home'))
        return data


class RecipeCreateUpdateMixin:
    model = Recipe
    form_class = RecipeCreateUpdateForm
    context_object_name = 'recipe'
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        recipe = self.object
        if recipe is not None:
            ingredient_qs = Ingredient.objects.filter(recipe=recipe)
            recipe_step_qs = RecipeStep.objects.filter(recipe=recipe)
        else:
            ingredient_qs = Ingredient.objects.none()
            recipe_step_qs = RecipeStep.objects.none()

        ingredient_formset = IngredientFormset(
            request.POST,
            queryset=ingredient_qs,
            prefix='ingredient-form',
        )
        recipe_step_formset = RecipeStepFormset(
            request.POST,
            queryset=recipe_step_qs,
            prefix='recipe-step-form'
        )

        formsets = (
            ingredient_formset,
            recipe_step_formset,
        )

        if self.validate_forms(formsets):
            return redirect(self.success_url)

        context = self.get_context_data(**kwargs)
        context.update(
            {
                'ingredient_formset': ingredient_formset,
                'recipe_step_formset': recipe_step_formset,
            }
        )

        return self.render_to_response(context)

    def validate_forms(self, formsets):
        form = self.get_form()
        if form.is_valid() and all(fset.is_valid() for fset in formsets):
            recipe = form.save()
            for formset in formsets:
                objects = formset.save(commit=False)
                for del_obj in formset.deleted_objects:
                    del_obj.delete()
                for obj in objects:
                    obj.recipe_id = recipe.pk
                    obj.save()
            return True
        return False

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return self.success_url


class RecipeCreateView(LoginRequiredMixin, RecipeCreateUpdateMixin, views.CreateView):
    template_name = 'main/recipe_create.html'

    def get(self, request, *args, **kwargs):
        super(RecipeCreateView, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        ingredient_formset = IngredientFormset(queryset=Ingredient.objects.none(), prefix='ingredient-form')
        recipe_step_formset = RecipeStepFormset(queryset=Ingredient.objects.none(), prefix='recipe-step-form')
        context.update(
            {
                'ingredient_formset': ingredient_formset,
                'recipe_step_formset': recipe_step_formset,
            }
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class RecipeUpdateView(LoginRequiredMixin, CheckCorrectUserMixin, RecipeCreateUpdateMixin, views.UpdateView):
    template_name = 'main/recipe_update.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        recipe = self.object
        context = self.get_context_data(**kwargs)
        ingredient_qs = Ingredient.objects.filter(recipe=recipe)
        recipe_step_qs = RecipeStep.objects.filter(recipe=recipe)
        ingredient_formset = IngredientFormset(queryset=ingredient_qs, prefix='ingredient-form')
        recipe_step_formset = RecipeStepFormset(queryset=recipe_step_qs, prefix='recipe-step-form')
        context.update(
            {
                'ingredient_formset': ingredient_formset,
                'recipe_step_formset': recipe_step_formset,
            }
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)




class RecipeDeleteView(LoginRequiredMixin, CheckCorrectUserMixin, views.DeleteView):
    model = Recipe
    template_name = 'main/recipe_delete.html'
    success_url = reverse_lazy('dashboard')


class RecipeDetailsView(views.DetailView):
    model = Recipe
    template_name = 'main/recipe_details.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailsView, self).get_context_data(**kwargs)
        ingredients = Ingredient.objects.filter(recipe=self.object)
        for ingredient in ingredients:
            print(ingredient)
        data = {
            'food_types': FoodType.objects.filter(recipe=self.object),
            'recipe_steps': RecipeStep.objects.filter(recipe=self.object),
            'ingredients': Ingredient.objects.filter(recipe=self.object),
        }
        context.update(data)
        return context


def like_button(request, pk, ):
    recipe = Recipe.objects.prefetch_related('likes').get(pk=pk)
    if request.user not in recipe.likes.all():
        recipe.likes.add(request.user)
    else:
        recipe.likes.remove(request.user)
        recipe.save()

    return redirect('recipe details', pk=recipe.pk)
