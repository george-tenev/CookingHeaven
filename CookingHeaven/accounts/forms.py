from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import signals
from django.dispatch import receiver

from CookingHeaven.accounts.models import CookingHeavenUser, Profile


class AbstractCookingHeavenUserCreationFrom(UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Enter password'
            }
        )

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password'
            }
        )

        self.fields['first_name'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Enter first name'
            }
        )

        self.fields['last_name'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Enter last name'
            }
        )

    def save(self, commit=True):
        user = super(AbstractCookingHeavenUserCreationFrom, self).save(commit=False)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user
        )
        if commit:
            user.save()
            profile.save()
        return user

    def clean(self):
        cleaned_data = super(AbstractCookingHeavenUserCreationFrom, self).clean()
        if not self.cleaned_data['first_name'].isalpha():
            self.add_error('first_name', "Enter only alphabetic symbols!")
        if not self.cleaned_data['last_name'].isalpha():
            self.add_error('first_name', "Enter only alphabetic symbols!")
        return cleaned_data


class UserRegisterForm(AbstractCookingHeavenUserCreationFrom):
    class Meta:
        model = CookingHeavenUser
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter username',
                },
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                },
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email'
                }
            )
        }

#
# class AdminProfileCreateForm(AbstractCookingHeavenUserCreationFrom):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     class Meta:
#         model = CookingHeavenUser
#         fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff']
#
#         widgets = {
#             'username': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter username',
#                 },
#             ),
#             'first_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter first name',
#                 },
#             ),
#             'last_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter last name',
#                 },
#             ),
#             'email': forms.EmailInput(
#                 attrs={
#                     'placeholder': 'Enter email'
#                 }
#             )
#         }


class SuperUserProfileCreationForm(AbstractCookingHeavenUserCreationFrom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        fields = '__all__'
        model = CookingHeavenUser

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter username',
                },
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                },
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email'
                }
            )
        }