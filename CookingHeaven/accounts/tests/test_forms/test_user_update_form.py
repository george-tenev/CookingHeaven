from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from CookingHeaven.accounts.forms import UserRegisterForm, UserUpdateForm
from CookingHeaven.accounts.models import Profile
from CookingHeaven.accounts.views import ProfileDetailsView
from CookingHeaven.main.models import Recipe

UserModel = get_user_model()


class TestUserUpdateForm(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qwe',
        'email': 'test@test.com',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'test',
        'last_name': 'test',
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

    def test_update_form_all_valid__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        form = UserUpdateForm(data={
            'username': 'newgeorgi',
            'email': 'georgi@mail.com',
            'first_name': 'georgi',
            'last_name': 'testov',
        }, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_profile = Profile.objects.get(pk=profile.pk)
        self.assertEqual(updated_profile.user.username, 'newgeorgi')
        self.assertEqual(updated_profile.user.email, 'georgi@mail.com')
        self.assertEqual(updated_profile.first_name, 'georgi')
        self.assertEqual(updated_profile.last_name, 'testov')

    def test_update_form__first_name_not_valid__expec_not_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        form = UserUpdateForm(data={
            'username': 'new georgi',
            'email': 'georgi@mail.com',
            'first_name': 'georgi',
            'last_name': 'testov',
        }, instance=user)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError) as context:
            form.save()
        updated_profile = Profile.objects.get(pk=profile.pk)
        self.assertEqual(updated_profile.user.username, self.VALID_USER_CREDENTIALS['username'])
        self.assertEqual(updated_profile.user.email, self.VALID_USER_CREDENTIALS['email'])
        self.assertEqual(updated_profile.first_name, self.VALID_PROFILE_DATA['first_name'])
        self.assertEqual(updated_profile.last_name, self.VALID_PROFILE_DATA['last_name'])