import os

from cloudinary import models as cloudinary_models
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from CookingHeaven.accounts.models import CookingHeavenUser
from CookingHeaven.common.validators import is_alpha, is_alpha_and_space

UserModel = get_user_model()


class Category(models.Model):
    NAME_MAX_LENGTH = 50
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=[is_alpha_and_space],
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
            is_alpha_and_space,
        ],
    )

    publisher = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)

    description = models.TextField(
        null=True,
        blank=True,
    )

    preparation_time = models.FloatField()

    cooking_time = models.FloatField()

    likes = models.ManyToManyField(
        to=UserModel,
        related_name="recipe_likes_set",
    )

    category = models.ManyToManyField(
        # null=True,
        blank=True,
        to=Category,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("publisher", "name")

    def __str__(self):
        return self.name


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.user)

    def count_likes(self):
        return self.likes.count()

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



class RecipeCloudinaryField(cloudinary_models.CloudinaryField):
    def pre_save(self, model_instance, add):
        self.options.update({"folder": os.getenv("APP_ENVIRONMENT", "Development")})
        return super(RecipeCloudinaryField, self).pre_save(model_instance, add)


class RecipePhoto(models.Model):
    photo = RecipeCloudinaryField()
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name="photos",
    )


class RecipeStep(models.Model):
    description = models.TextField()
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)


class Unit(models.Model):
    NAME_MAX_LENGTH = 60
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=[
            is_alpha,
        ],
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=[is_alpha_and_space],
    )
    amount = models.PositiveIntegerField()

    unit = models.ForeignKey(blank=True, null=True, to=Unit, on_delete=models.PROTECT)

    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("recipe", "name")

    def __str__(self):
        return self.name
