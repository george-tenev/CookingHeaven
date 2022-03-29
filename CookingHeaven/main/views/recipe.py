from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from CookingHeaven.main.forms import RecipeCreateForm, IngredientFormset, RecipeStepFormset, RecipeUpdateForm
from CookingHeaven.main.models import Recipe, Ingredient, RecipeStep


class RecipeCreateView(LoginRequiredMixin, views.CreateView):
    model = Recipe
    template_name = 'main/recipe_create.html'
    form_class = RecipeCreateForm
    context_object_name = 'recipe'
    success_url = reverse_lazy('home')

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
        form = self.get_form()
        ingredient_formset = IngredientFormset(
            request.POST,
            queryset=Ingredient.objects.none(),
            prefix='ingredient-form'
        )
        recipe_step_formset = RecipeStepFormset(
            request.POST,
            queryset=Ingredient.objects.none(),
            prefix='recipe-step-form'
        )
        formsets = (
            ingredient_formset,
            recipe_step_formset,
        )
        if form.is_valid():
            if all(all(f.is_valid() for f in fset) for fset in formsets):
                recipe = form.save()
                for formset in formsets:
                    for f in formset:
                        form_obj = f.save(commit=False)
                        form_obj.recipe_id = recipe.pk
                        form_obj.save()
                return redirect(reverse_lazy('home'))

        context = self.get_context_data(**kwargs)
        context.update(
            {
                'ingredient_formset': ingredient_formset,
                'recipe_step_formset': recipe_step_formset,
            }
        )

        return self.render_to_response(context)

    def get_form_kwargs(self):
        kwargs = super(RecipeCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return self.success_url


class RecipeUpdateView(LoginRequiredMixin, views.UpdateView):
    model = Recipe
    template_name = 'main/recipe_update.html'
    form_class = RecipeUpdateForm
    context_object_name = 'recipe'
    success_url = reverse_lazy('home')

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
        recipe = self.object
        form = self.get_form()

        ingredient_qs = Ingredient.objects.filter(recipe=recipe)
        recipe_step_qs = RecipeStep.objects.filter(recipe=recipe)

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

        if form.is_valid() and all(fset.is_valid() for fset in formsets):
            form.save()
            for formset in formsets:
                formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                formset.recipe_id = recipe.pk
                formset.save()
                return redirect(reverse_lazy('home'))

        context = self.get_context_data(**kwargs)
        context.update(
            {
                'ingredient_formset': ingredient_formset,
                'recipe_step_formset': recipe_step_formset,
            }
        )

        return self.render_to_response(context)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return self.success_url


class RecipeDeleteView(LoginRequiredMixin, views.DeleteView):
    model = Recipe
    template_name = 'main/recipe_delete.html'
    success_url = reverse_lazy('dashboard')


class RecipeDetailsView(views.DetailView):
    model = Recipe
    template_name = 'main/recipe_delete.html'
    context_object_name = 'recipe'
