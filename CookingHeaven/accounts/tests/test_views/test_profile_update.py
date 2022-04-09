from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from CookingHeaven.accounts.models import Profile
from CookingHeaven.accounts.views import ProfileDetailsView
from CookingHeaven.main.models import Recipe

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
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

    def test_update_profile__when_all_valid__expect_to_update(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.client.post(
            reverse('profile update', kwargs={'pk': profile.pk}),
            data={
                'first_name': 'newfirst',
                'last_name': 'newlast',

                  },
        )
        updated_profile = Profile.objects.get(pk=profile.pk)
        self.assertEqual(updated_profile.first_name, 'newfirst')
        self.assertEqual(updated_profile.last_name, 'newlast')

    def test_update_profile__when_all_valid__expect_to_redirect_to_profile_details(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse(
            'profile update',
            kwargs={
                'pk': profile.pk,
            }
        ),
            data={
                'first_name': 'newfirstname',
                'last_name': 'newlastname'}
        )
        expected_url = reverse('profile details', kwargs={'pk': profile.pk})
        self.assertRedirects(response, expected_url)