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


class RecipeCreateTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qwe',
        'email': 'test@test.com',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'test',
        'last_name': 'test',
    }

    VALID_RECIPE_FORM_DATA = {
        'name': ['testrecipe'],
        'description': [''],
        'preparation_time': ['1'],
        'cooking_time': ['1'],
        'ingredient-form-TOTAL_FORMS': ['0'],
        'ingredient-form-INITIAL_FORMS': ['0'],
        'ingredient-form-MIN_NUM_FORMS': ['0'],
        'ingredient-form-MAX_NUM_FORMS': ['1000'],
        'ingredient-form-__prefix__-name': [''],
        'ingredient-form-__prefix__-amount': [''],
        'ingredient-form-__prefix__-unit': [''],
        'ingredient-form-__prefix__-id': [''],
        'recipe-step-form-TOTAL_FORMS': ['0'],
        'recipe-step-form-INITIAL_FORMS': ['0'],
        'recipe-step-form-MIN_NUM_FORMS': ['0'],
        'recipe-step-form-MAX_NUM_FORMS': ['1000'],
        'recipe-step-form-__prefix__-description': [''],
        'recipe-step-form-__prefix__-id': ['']
    }

    UNVALID_RECIPE_FORM_DATA = {
        'name': [''],
        'description': [''],
        'preparation_time': [''],
        'cooking_time': [''],
        'ingredient-form-TOTAL_FORMS': ['0'],
        'ingredient-form-INITIAL_FORMS': ['0'],
        'ingredient-form-MIN_NUM_FORMS': ['0'],
        'ingredient-form-MAX_NUM_FORMS': ['1000'],
        'ingredient-form-__prefix__-name': [''],
        'ingredient-form-__prefix__-amount': [''],
        'ingredient-form-__prefix__-unit': [''],
        'ingredient-form-__prefix__-id': [''],
        'recipe-step-form-TOTAL_FORMS': ['0'],
        'recipe-step-form-INITIAL_FORMS': ['0'],
        'recipe-step-form-MIN_NUM_FORMS': ['0'],
        'recipe-step-form-MAX_NUM_FORMS': ['1000'],
        'recipe-step-form-__prefix__-description': [''],
        'recipe-step-form-__prefix__-id': ['']
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

    def test_create_recipe__all_valid(self):
        self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        with open(BASE_DIR / 'imagetest.jpg', mode='rb') as photo:
            response = self.client.post(
                reverse('recipe create'),
                data={
                    'photo': photo,
                    **self.VALID_RECIPE_FORM_DATA
                }
            )
        recipe = Recipe.objects.first()
        self.assertIsNotNone(recipe)


    def test_create_recipe__not_logged_in__expectd_redirect_to_log_in(self):
        with open(BASE_DIR / 'imagetest.jpg', mode='rb') as photo:
            response = self.client.post(
                reverse('recipe create'),
                data={
                    'photo': photo,
                    **self.VALID_RECIPE_FORM_DATA
                }
            )
        self.assertEqual(response.status_code, 302)

    def test_create_recipe__not_valid__expect_fail(self):
        with open(BASE_DIR / 'imagetest.jpg', mode='rb') as photo:
            response = self.client.post(
                reverse('recipe create'),
                data={
                    'photo': photo,
                    **self.UNVALID_RECIPE_FORM_DATA
                }
            )

        recipe = Recipe.objects.first()
        self.assertIsNone(recipe)

    def test_create_recipe__all_valid__epecetd_success_url_dashboard(self):
        self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        with open(BASE_DIR / 'imagetest.jpg', mode='rb') as photo:
            response = self.client.post(
                reverse('recipe create'),
                data={
                    'photo': photo,
                    **self.VALID_RECIPE_FORM_DATA
                }
            )
        recipe = Recipe.objects.first()
        self.assertRedirects(response, reverse('dashboard'))

