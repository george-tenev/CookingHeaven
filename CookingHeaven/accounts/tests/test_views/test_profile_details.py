from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from CookingHeaven.accounts.models import Profile
from CookingHeaven.accounts.views import ProfileDetailsView
from CookingHeaven.main.models import Recipe

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
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

    def test_when_not_logged_in_opening_profile_expect_302(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": profile.pk,
                },
            )
        )
        self.assertEqual(302, response.status_code)

    def test_logged_in_opening_not_exising_profile__expect_redirect_to_400(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": 100,
                },
            )
        )
        self.assertEqual("/error_page/", response.url)

    def test_expect_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()

        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": profile.pk,
                },
            )
        )
        self.assertTemplateUsed(ProfileDetailsView.template_name)

    def test_when_no_recipes__recipes_should_be_empty(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": profile.pk,
                },
            )
        )
        self.assertListEqual([], response.context_data["recipes"])

    def test_when_recipes__should_return_owner_recipes(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = self.__create_recipe(user, **self.VALID_RECIPE_DATA)
        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": profile.pk,
                },
            )
        )
        self.assertListEqual(
            [
                recipe,
            ],
            response.context["recipes"],
        )

    def test_when_recipes_and_no_likes__total_likes_should_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = self.__create_recipe(user, **self.VALID_RECIPE_DATA)
        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": profile.pk,
                },
            )
        )
        total_likes = sum(
            recipe.likes.count() for recipe in response.context["recipes"]
        )
        self.assertEqual(0, total_likes)

    def test_when_recipe_and_like__total_likes_should_be_1(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = self.__create_recipe(user, **self.VALID_RECIPE_DATA)
        recipe.likes.add(user)
        recipe.save()
        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": profile.pk,
                },
            )
        )
        total_likes = sum(
            recipe.likes.count() for recipe in response.context["recipes"]
        )
        self.assertEqual(1, total_likes)

    def test_when_no_recipes__likes_should_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(
            reverse(
                "profile details",
                kwargs={
                    "pk": profile.pk,
                },
            )
        )
        total_likes = sum(
            recipe.likes.count() for recipe in response.context["recipes"]
        )
        self.assertEqual(0, total_likes)

    def test_when_not_owner__raise_permision_error(self):
        user, profile = self.__create_valid_user_and_profile()
        user_creds = {
            "username": "testuser2",
            "password": "12345qwe2",
            "email": "testuser2@user.com",
        }
        user2 = self.__create_user(**user_creds)
        self.client.login(**user_creds)
        try:
            response = self.client.get(
                reverse(
                    "profile details",
                    kwargs={
                        "pk": profile.pk,
                    },
                )
            )
        except PermissionError as ex:
            self.assertRaises(PermissionError)
