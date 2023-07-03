from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from CookingHeaven.accounts.models import Profile
from CookingHeaven.main.models import Category, Recipe

UserModel = get_user_model()


class TestGenericViews(TestCase):
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
        "photo": "/imagetest.jpg",
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

    def test_home_view_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe1 = self.__create_recipe(
            user=user, **{"name": "testrecipe", **self.VALID_RECIPE_DATA}
        )
        recipe2 = self.__create_recipe(
            user=user, **{"name": "recipe", **self.VALID_RECIPE_DATA}
        )
        recipe3 = self.__create_recipe(
            user=user, **{"name": "test", **self.VALID_RECIPE_DATA}
        )
        recipe4 = self.__create_recipe(
            user=user, **{"name": "recipetest", **self.VALID_RECIPE_DATA}
        )
        response = self.client.get(reverse("home"))
        self.assertListEqual(
            [recipe4, recipe3, recipe2], list(response.context_data["recipes"])
        )

    def test_home_view_no_recipes(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse("home"))
        self.assertListEqual([], list(response.context_data["recipes"]))

    def test_dashboard_view_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe1 = self.__create_recipe(
            user=user, **{"name": "testrecipe", **self.VALID_RECIPE_DATA}
        )
        recipe2 = self.__create_recipe(
            user=user, **{"name": "recipe", **self.VALID_RECIPE_DATA}
        )
        recipe3 = self.__create_recipe(
            user=user, **{"name": "test", **self.VALID_RECIPE_DATA}
        )
        recipe4 = self.__create_recipe(
            user=user, **{"name": "recipetest", **self.VALID_RECIPE_DATA}
        )
        response = self.client.get(reverse("dashboard"))
        self.assertListEqual(
            [recipe4, recipe3, recipe2], list(response.context_data["recipes"])
        )

    def test_dashboard_view_no_recipes(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse("dashboard"))
        self.assertListEqual([], list(response.context_data["recipes"]))
