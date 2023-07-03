from unittest.mock import Mock

from django import test as django_test
from django.contrib.auth import get_user_model
from django.core import files
from django.urls import reverse, reverse_lazy

from CookingHeaven.accounts.models import Profile, CookingHeavenUser
from django.core.files.uploadedfile import SimpleUploadedFile
from CookingHeaven.main.models import Recipe
from CookingHeaven.settings import BASE_DIR

UserModel = get_user_model()


class RecipeDeleteViewTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        "username": "testuser",
        "password": "12345qwe",
        "email": "test@test.com",
    }

    VALID_PROFILE_DATA = {
        "first_name": "test",
        "last_name": "test",
    }

    VALID_RECIPE_DATA = {
        "name": "testrecipe",
        "photo": "asd.jpg",
        "preparation_time": 1,
        "cooking_time": 1,
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return user, profile

    def __create_recipe(self, user, **recipe_data):
        recipe = Recipe.objects.create(**recipe_data, publisher=user)
        return recipe

    def test_like__button_view__expect_liked(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse("recipe like", kwargs={"pk": recipe.pk}))
        likes = recipe.likes.all()
        self.assertListEqual([user], list(likes))

    def test_like_recipe__unklike(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.get(reverse("recipe like", kwargs={"pk": recipe.pk}))
        self.client.get(reverse("recipe like", kwargs={"pk": recipe.pk}))
        likes = recipe.likes.all()
        self.assertListEqual([], list(likes))

    def test_like_recipe__expect_redirect_recipe_details(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse("recipe like", kwargs={"pk": recipe.pk}))
        likes = recipe.likes.all()
        self.assertRedirects(
            response, reverse("recipe details", kwargs={"pk": recipe.pk})
        )
