from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from CookingHeaven.accounts.models import Profile
from CookingHeaven.main.models import Category, Unit, Ingredient, Recipe

UserModel = get_user_model()


class IngredientModelTests(TestCase):
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

    def __create_unit(self):
        unit = Unit.objects.create(name="gram")
        return unit

    def test_ingredient_model__all_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        unit = self.__create_unit()
        data = {
            "name": "test",
            "amount": 1,
            "unit": unit,
            "recipe": recipe,
        }
        ingredient = Ingredient.objects.create(**data)
        self.assertTrue(isinstance(ingredient, Ingredient))

    def test_ingredient_model__all_valid_str(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        unit = self.__create_unit()
        data = {
            "name": "test",
            "amount": 1,
            "unit": unit,
            "recipe": recipe,
        }
        ingredient = Ingredient.objects.create(**data)
        self.assertEqual(str(ingredient), data["name"])

    # def test_category_model__name_not_valid(self):
    #     ingredient = Ingredient.objects.create(name='gram123')
    #     with self.assertRaises(ValidationError) as context:
    #         ingredient.full_clean()
    #         ingredient.save()
    #     self.assertIsNotNone(context.exception)
