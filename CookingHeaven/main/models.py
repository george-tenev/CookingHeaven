from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.forms.models import inlineformset_factory, formset_factory, modelform_factory, modelformset_factory



from CookingHeaven.accounts.models import CookingHeavenUser
from CookingHeaven.common.validators import is_alpha


class FoodType(models.Model):
    NAME_MAX_LENGTH = 50
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=[is_alpha],
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=[
            MinLengthValidator(NAME_MIN_LENGTH),
            is_alpha,
        ]
    )

    publisher = models.ForeignKey(
        to=CookingHeavenUser,
        on_delete=models.CASCADE
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    photo = models.ImageField(
        upload_to='recipe'
    )

    preparation_time = models.FloatField()

    cooking_time = models.FloatField()

    likes = models.ManyToManyField(
        to=CookingHeavenUser,
        related_name='recipe_likes_set',
    )

    types = models.ManyToManyField(
        to=FoodType,
    )

    class Meta:
        unique_together = ('publisher', 'name')

    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    description = models.TextField()
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE
    )


class Unit(models.Model):
    NAME_MAX_LENGTH = 60
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=[is_alpha],
    )
    amount = models.PositiveIntegerField()

    unit = models.ForeignKey(
        to=Unit,
        on_delete=models.PROTECT
    )

    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('recipe', 'name')

    def __str__(self):
        return self.name
