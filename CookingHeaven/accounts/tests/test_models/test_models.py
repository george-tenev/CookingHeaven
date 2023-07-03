from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from CookingHeaven.accounts.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):
    VALID_USER_CREDENTIALS = {
        "username": "testuser",
        "password": "12345qwe",
        "email": "test@test.com",
    }

    VALID_PROFILE_DATA = {
        "first_name": "test",
        "last_name": "test",
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

    def test_profile_create__when_all_valid__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_not_only_letters__expect_to_fail(
        self,
    ):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            first_name="Georgi1",
            last_name=self.VALID_PROFILE_DATA["last_name"],
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_length_is_too_short__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            first_name="G",
            last_name=self.VALID_PROFILE_DATA["last_name"],
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_not_only_letters__expect_to_fail(
        self,
    ):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            first_name=self.VALID_PROFILE_DATA["first_name"],
            last_name="Georgiev1",
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        user, profile = self.__create_valid_user_and_profile()

        expected_fullname = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(expected_fullname, profile.full_name)

    def test_profile_str__when_valid__expect_correct_str(self):
        user, profile = self.__create_valid_user_and_profile()

        expected_str = f'{self.VALID_PROFILE_DATA["first_name"]}'
        self.assertEqual(expected_str, str(profile))


class TestUserModel(TestCase):
    VALID_USER_CREDENTIALS = {
        "username": "testuser",
        "password": "12345qwe",
        "email": "test@test.com",
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def test_user_all_valid(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        self.assertTrue(isinstance(user, UserModel))
        self.assertEqual(user.email, self.VALID_USER_CREDENTIALS["email"])
        self.assertEqual(user.username, self.VALID_USER_CREDENTIALS["username"])
