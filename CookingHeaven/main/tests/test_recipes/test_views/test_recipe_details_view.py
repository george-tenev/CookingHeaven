from unittest.mock import Mock

from django import test as django_test
from django.contrib.auth import get_user_model
from django.core import files
from django.urls import reverse, reverse_lazy

from CookingHeaven.accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from CookingHeaven.main.models import Recipe, Unit, Ingredient, RecipeStep, Category
from CookingHeaven.settings import BASE_DIR

UserModel = get_user_model()


class TestRecipeDetailsView(django_test.TestCase):
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

    def test_recipe_details_view__all_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        category = Category.objects.create(name="salad")
        recipe.category.add(category)
        unit = Unit.objects.create(name="gram")

        ingredient = Ingredient.objects.create(
            name="tomato", unit=unit, amount=1, recipe=recipe
        )
        recipe_step = RecipeStep.objects.create(recipe=recipe, description="Stir")
        response = self.client.get(reverse("recipe details", kwargs={"pk": recipe.pk}))
        self.assertListEqual(list(response.context_data["categories"]), [category])
        self.assertListEqual(list(response.context_data["ingredients"]), [ingredient])
        self.assertListEqual(list(response.context_data["recipe_steps"]), [recipe_step])

    def test_recipe_details_view__no_category__expect_no_category(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        response = self.client.get(reverse("recipe details", kwargs={"pk": recipe.pk}))
        self.assertListEqual(list(response.context_data["categories"]), [])

    def test_recipe_details_view__no_ingredient__expect_no_ingredient(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        response = self.client.get(reverse("recipe details", kwargs={"pk": recipe.pk}))
        self.assertListEqual(list(response.context_data["ingredients"]), [])

    def test_recipe_details_view__no_recipe_step__expect_no_recipe_step(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        response = self.client.get(reverse("recipe details", kwargs={"pk": recipe.pk}))
        self.assertListEqual(list(response.context_data["recipe_steps"]), [])
