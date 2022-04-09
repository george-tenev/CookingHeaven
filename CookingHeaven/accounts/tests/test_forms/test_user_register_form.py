from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from CookingHeaven.accounts.forms import UserRegisterForm
from CookingHeaven.accounts.models import Profile
from CookingHeaven.accounts.views import ProfileDetailsView
from CookingHeaven.main.models import Recipe

UserModel = get_user_model()


class ProfileFormsTests(django_test.TestCase):
    VALID_USER_REGISTER = {
            'first_name': 'georgi',
            'last_name': 'georgiev',
            'username': 'georgi1234@',
            'password1': 'TestPass123@',
            'password2': 'TestPass123@',
            'email': 'georgi@test.com'
            }
    FIRST_NAME_UNVALID_USER_REGISTER = {
        'first_name': 'georgi1',
        'last_name': 'georgiev',
        'username': 'georgi1234@',
        'password1': 'TestPass123@',
        'password2': 'TestPass123@',
        'email': 'georgi@test.com'
    }

    def test_user_register_form_first_name_not_only_alpha(self):
        form = UserRegisterForm(data=self.FIRST_NAME_UNVALID_USER_REGISTER)
        self.assertFalse(form.is_valid())
    def test_user_register_form_last_name_not_only_alpha(self):
        form = UserRegisterForm({
        'first_name': 'georgi',
        'last_name': 'georgiev1',
        'username': 'georgi1234@',
        'password1': 'TestPass123@',
        'password2': 'TestPass123@',
        'email': 'georgi@test.com'
    })
        self.assertFalse(form.is_valid())

    def test_user_register_form_username_has_space(self):
        form = UserRegisterForm(data={
        'first_name': 'georgi',
        'last_name': 'georgiev',
        'username': 'georgi 1234@',
        'password1': 'TestPass123@',
        'password2': 'TestPass123@',
        'email': 'georgi@test.com'
    })

        self.assertFalse(form.is_valid())

    def test_user_register_form_passwords_do_not_match(self):
        form = UserRegisterForm(data={
        'first_name': 'georgi',
        'last_name': 'georgiev',
        'username': 'georgi1234@',
        'password1': 'TestPass123@',
        'password2': 'TestPPass123@',
        'email': 'georgi@test.com'
    })

        self.assertFalse(form.is_valid())

    def test_user_register_form_email_invalid(self):
        form = UserRegisterForm(data={
        'first_name': 'georgi',
        'last_name': 'georgiev',
        'username': 'georgi1234@',
        'password1': 'TestPass123@',
        'password2': 'TestPass123@',
        'email': 'georgi.com'
    })

        self.assertFalse(form.is_valid())

    def test_user_register_form__all_valid(self):
        form = UserRegisterForm(data=self.VALID_USER_REGISTER)
        self.assertTrue(form.is_valid())


