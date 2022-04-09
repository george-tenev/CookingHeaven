from unittest.mock import Mock

from django import test as django_test
from django.contrib.auth import get_user_model
from django.core import files
from django.urls import reverse, reverse_lazy

from CookingHeaven.accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from CookingHeaven.main.models import Recipe
from CookingHeaven.settings import BASE_DIR

UserModel = get_user_model()


class RecipeDeleteViewTests(django_test.TestCase):

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

    def test_delete_recipe_owner__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.post(reverse('recipe delete', kwargs={'pk': recipe.pk}))
        deleted_recipe = list(Recipe.objects.filter(pk=recipe.pk))
        self.assertListEqual(deleted_recipe, [])

    def test_delete_recipe_not_owner__expect_recipe_not_deleted_and_raise_permission_error(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials ={
            'username': 'testuser2',
            'password': '12345qwe',
            'email': 'test@test2.com',
        }
        user2 = self.__create_user(**credentials)

        expected_recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.client.login(**credentials)
        with self.assertRaises(PermissionError) as context:
            self.client.post(reverse('recipe delete', kwargs={'pk': expected_recipe.pk}))

        recipe = list(Recipe.objects.filter(pk=expected_recipe.pk))

        self.assertListEqual([expected_recipe], recipe)


    def test_delete_recipe__not_owner__is_staff_true_expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials ={
            'username': 'testuser2',
            'password': '12345qwe',
            'email': 'test@test2.com',
        }
        user2 = self.__create_user(**credentials)
        user2.is_staff = True
        user2.save()
        recipe = self.__create_recipe(user=user, **self.VALID_RECIPE_DATA)
        self.client.login(**credentials)
        self.client.post(reverse('recipe delete', kwargs={'pk': recipe.pk}))

        deleted_recipe = list(Recipe.objects.filter(pk=recipe.pk))

        self.assertListEqual(deleted_recipe, [])
