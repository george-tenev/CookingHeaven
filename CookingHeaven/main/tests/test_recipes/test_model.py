from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from CookingHeaven.accounts.models import Profile
from CookingHeaven.main.models import Category, Recipe

UserModel = get_user_model()



class RecipeModelTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qwe',
        'email': 'test@test.com',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'test',
        'last_name': 'test',
    }

    VALID_RECIPE_DATA = {
        'name': 'testrecipe',
        'photo': 'asd.jpg',
        'preparation_time': 1,
        'cooking_time': 1,
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

    def test_recipe__all_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.assertTrue(isinstance(recipe, Recipe))

    def test_recipe__all_valid_str(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.assertEqual(str(recipe), self.VALID_RECIPE_DATA['name'])

    def test_recipe__name_not_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        data = {
        'name': 'testrecipe1',
        'photo': 'asd.jpg',
        'preparation_time': 1,
        'cooking_time': 1,
    }
        recipe = Recipe(publisher=user, **data)
        with self.assertRaises(ValidationError) as context:
            recipe.full_clean()  # This is called in ModelForms implicitly
            recipe.save()

        self.assertIsNotNone(context.exception)
