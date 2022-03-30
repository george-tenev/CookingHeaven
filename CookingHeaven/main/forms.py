from django import forms
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet

from CookingHeaven.main.models import Recipe, Ingredient, RecipeStep


class RecipeCreateForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RecipeCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        recipe = super(RecipeCreateForm, self).save(commit=False)
        recipe.publisher = self.user
        if commit:
            recipe.save()
            self.save_m2m()
        return recipe

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'photo', 'preparation_time', 'cooking_time', 'types',)


class RecipeUpdateForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        recipe = super().save(commit=False)
        recipe.publisher = self.user
        if commit:
            recipe.save()
            self.save_m2m()
        return recipe

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'photo', 'preparation_time', 'cooking_time', 'types',)


class IngredientCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Ingredient
        fields = ('name', 'amount', 'unit',)


class RecipeStepCreateForm(ModelForm):
    class Meta:
        model = RecipeStep
        fields = ('description',)


class CustomModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


IngredientFormset = modelformset_factory(
    Ingredient,
    form=IngredientCreateForm,
    formset=CustomModelFormSet,
    can_delete=True,
    extra=0
)
RecipeStepFormset = modelformset_factory(
    RecipeStep,
    form=RecipeStepCreateForm,
    formset=CustomModelFormSet,
    can_delete=True,
    extra=0
)
