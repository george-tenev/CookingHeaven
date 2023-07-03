from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from CookingHeaven.accounts.models import Profile
from CookingHeaven.accounts.views import ProfileDetailsView
from CookingHeaven.main.models import Recipe

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
    VALID_USER_REGISTER = {
        "first_name": "georgi",
        "last_name": "georgiev",
        "username": "georgi1234@",
        "password1": "TestPass123@",
        "password2": "TestPass123@",
        "email": "georgi@test.com",
    }
    FIRST_NAME_UNVALID_USER_REGISTER = {
        "first_name": "georgi1",
        "last_name": "georgiev",
        "username": "georgi1234@",
        "password1": "TestPass123@",
        "password2": "TestPass123@",
        "email": "georgi@test.com",
    }

    def test_all_valid__expect_logged_in(self):
        response = self.client.post(reverse("register"), data=self.VALID_USER_REGISTER)
        user = UserModel.objects.get(username=self.VALID_USER_REGISTER["username"])
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_unvalid__expect_not_logged_in(self):
        response = self.client.post(
            reverse("register"), data=self.FIRST_NAME_UNVALID_USER_REGISTER
        )
        user = UserModel.objects.filter(
            username=self.FIRST_NAME_UNVALID_USER_REGISTER["username"]
        ).first()
        self.assertIsNone(user)
        self.assertNotIn("_auth_user_id", self.client.session)
