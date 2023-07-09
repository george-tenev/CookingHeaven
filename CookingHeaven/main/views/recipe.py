import cloudinary
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views, View
from django.views.generic.detail import SingleObjectMixin

from CookingHeaven.main.forms import (
    IngredientFormset,
    RecipeStepFormset,
    RecipePhotoFormSet,
    RecipeCreateUpdateForm,
    CommentForm,
)
from CookingHeaven.main.models import (
    Recipe,
    Ingredient,
    RecipeStep,
    Category,
    RecipePhoto,
    Comment,
)


class RecipeCheckCorrectUserMixin:
    def dispatch(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user != recipe.publisher and not request.user.is_staff:
            raise PermissionError("You have no permission for this page")
        return super(RecipeCheckCorrectUserMixin, self).dispatch(
            request, *args, **kwargs
        )


class RecipeCreateUpdateMixin:
    model = Recipe
    form_class = RecipeCreateUpdateForm
    context_object_name = "recipe"
    success_url = reverse_lazy("dashboard")

    def get_formsets(self, recipe, request_method=None, request_files=None):
        ingredient_qs = Ingredient.objects.filter(recipe=recipe)
        recipe_step_qs = RecipeStep.objects.filter(recipe=recipe)
        recipe_photo_qs = RecipePhoto.objects.filter(recipe=recipe)

        ingredient_formset = IngredientFormset(
            request_method,
            queryset=ingredient_qs,
            prefix="ingredient-form",
        )

        recipe_step_formset = RecipeStepFormset(
            request_method, queryset=recipe_step_qs, prefix="recipe-step-form"
        )

        recipe_photo_formset = RecipePhotoFormSet(
            request_method,
            request_files,
            queryset=recipe_photo_qs,
            prefix="recipe-photo-form",
        )

        formsets = {
            "ingredient_formset": ingredient_formset,
            "recipe_step_formset": recipe_step_formset,
            "recipe_photo_formset": recipe_photo_formset,
        }

        return formsets

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

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        formsets = self.get_formsets(self.object)
        context = self.get_context_data(**kwargs)
        context.update(formsets)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        formsets = self.get_formsets(self.object, request.POST, request.FILES)

        if self.validate_forms(formsets.values()):
            return redirect(self.success_url)

        context = self.get_context_data(**kwargs)
        context.update(formsets)

        return self.render_to_response(context)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class RecipeCreateView(LoginRequiredMixin, RecipeCreateUpdateMixin, views.CreateView):
    template_name = "main/recipe_create.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class RecipeUpdateView(
    LoginRequiredMixin,
    RecipeCheckCorrectUserMixin,
    RecipeCreateUpdateMixin,
    views.UpdateView,
):
    template_name = "main/recipe_update.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class RecipeDeleteView(
    LoginRequiredMixin, RecipeCheckCorrectUserMixin, views.DeleteView
):
    model = Recipe
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        for recipe_photo in self.object.photos.all():
            cloudinary.uploader.destroy(recipe_photo.photo.public_id, invalidate=True)
        return super(RecipeDeleteView, self).form_valid(form)


class RecipeDetailsView(views.DetailView):
    model = Recipe
    template_name = "main/recipe_details.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        comments = Comment.objects.filter(
            recipe=recipe, parent=None
        )  # we only get the parent comments
        replies = Comment.objects.filter(recipe=recipe).exclude(
            parent=None
        )  # all other comments are replies


        comment_form = CommentForm()

        data = {
            "categories": Category.objects.filter(recipe=self.object),
            "recipe_steps": RecipeStep.objects.filter(recipe=self.object),
            "ingredients": Ingredient.objects.filter(recipe=self.object),
            "comments": comments,
            "replies": replies,
            "comment_form": comment_form,
        }
        context.update(data)
        return context

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            print('-------------------------------------------------------------------------------Reached here')
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                body = comment_form.cleaned_data['body']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent = None

            new_comment = Comment(body=body, user=self.request.user, recipe=self.get_object(),
                                  parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)

class RecipeSearchView(views.ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "main/recipe_search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        vector = SearchVector(
            "name",
            "category",
            "description",
            StringAgg("ingredient__name", delimiter=" "),
        )
        recipes = Recipe.objects.annotate(
            rank=SearchRank(vector, SearchQuery(query))
        ).order_by("-rank")
        return recipes


class LikeButtonView(LoginRequiredMixin, View, SingleObjectMixin):
    model = Recipe

    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user not in recipe.likes.all():
            recipe.likes.add(request.user)
        else:
            recipe.likes.remove(request.user)
            recipe.save()

        return redirect(reverse("recipe details", kwargs={"pk": recipe.pk}))
