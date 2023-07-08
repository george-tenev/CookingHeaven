from django import forms
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet
from django.utils.translation import gettext_lazy as _

from CookingHeaven.main.models import (
    Recipe,
    Ingredient,
    RecipeStep,
    Category,
    Unit,
    RecipePhoto,
    Comment,
)
from cloudinary.forms import CloudinaryFileField


class RecipeCreateUpdateForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["preparation_time"].label = "Preparation time in minutes:"
        self.fields["cooking_time"].label = "Cooking time in minutes:"

    def save(self, commit=True, *args, **kwargs):
        recipe = super().save(commit=False)
        recipe.publisher = self.user
        if commit:
            recipe.save()
            self.save_m2m()
        return recipe

    class Meta:
        model = Recipe
        fields = (
            "name",
            "description",
            "preparation_time",
            "cooking_time",
            "category",
        )


class IngredientCreateForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = (
            "name",
            "amount",
            "unit",
        )


class RecipeStepCreateForm(ModelForm):
    class Meta:
        model = RecipeStep
        fields = ("description",)


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class UnitCreateForm(ModelForm):
    class Meta:
        model = Unit
        fields = "__all__"


class CustomModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class RecipeCategoryFilterForm(forms.Form):
    filter = forms.ChoiceField(choices=[])  # Initialize with empty choices

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["filter"].choices = [
            (category, category) for category in Category.objects.all()
        ]


IngredientFormset = modelformset_factory(
    Ingredient,
    form=IngredientCreateForm,
    formset=CustomModelFormSet,
    can_delete=True,
    extra=0,
)

RecipeStepFormset = modelformset_factory(
    RecipeStep,
    form=RecipeStepCreateForm,
    formset=CustomModelFormSet,
    can_delete=True,
    extra=0,
)


class RecipePhotoForm(forms.ModelForm):
    photo = CloudinaryFileField(
        options={
            "crop": "scale",
            "width": 800,
            "height": 600,
        }
    )

    class Meta:
        model = RecipePhoto
        fields = ("photo",)


RecipePhotoFormSet = forms.modelformset_factory(
    RecipePhoto,
    form=RecipePhotoForm,
    formset=CustomModelFormSet,
    can_delete=True,
    extra=0,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['body', 'parent']

        labels = {
            'body': _(''),
        }

        widgets = {
            'body': forms.TextInput(),
        }