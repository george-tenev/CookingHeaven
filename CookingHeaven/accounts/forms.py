from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db.models import signals
from django.dispatch import receiver
from django.forms import ModelForm

from CookingHeaven.accounts.models import CookingHeavenUser, Profile

UserModel = get_user_model()






class AbstractCookingHeavenUserForm(UserCreationForm):
    FIRST_NAME_ERROR_MESSAGE = "Enter only alphabetic symbols!"
    LAST_NAME_ERROR_MESSAGE = "Enter only alphabetic symbols!"

    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        user = super().save(commit=False)

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
        cleaned_data = super().clean()
        if not self.cleaned_data['first_name'].isalpha():
            self.add_error('first_name', self.FIRST_NAME_ERROR_MESSAGE)
        if not self.cleaned_data['last_name'].isalpha():
            self.add_error('first_name', self.LAST_NAME_ERROR_MESSAGE)
        return cleaned_data




class UserRegisterForm(AbstractCookingHeavenUserForm):

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
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

    class Meta:
        model = UserModel
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
            ),
        }


class UserUpdateForm(UserChangeForm):
    FIRST_NAME_ERROR_MESSAGE = "Enter only alphabetic symbols!"
    LAST_NAME_ERROR_MESSAGE = "Enter only alphabetic symbols!"

    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.profile = Profile.objects.get(user=self.instance)
        self.fields['first_name'].initial = self.profile.first_name
        self.fields['last_name'].initial = self.profile.last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.profile.first_name = self.cleaned_data['first_name']
            self.profile.last_name = self.cleaned_data['last_name']
            self.profile.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        if not self.cleaned_data['first_name'].isalpha():
            self.add_error('first_name', self.FIRST_NAME_ERROR_MESSAGE)
        if not self.cleaned_data['last_name'].isalpha():
            self.add_error('first_name', self.LAST_NAME_ERROR_MESSAGE)
        return cleaned_data


    class Meta:
        model = UserModel
        fields = ['username', 'email']
        # exclude = ['password']
        # exclude = ['password1', 'password2']
        # widgets = {
        #     'username': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter username',
        #         },
        #     ),
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter first name',
        #         },
        #     ),
        #     'last_name': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter last name',
        #         },
        #     ),
        #     'email': forms.EmailInput(
        #         attrs={
        #             'placeholder': 'Enter email'
        #         }
        #     )
        # }


class SuperUserProfileCreationForm(AbstractCookingHeavenUserForm):
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

    class Meta:
        exclude = ['last_login', 'password',]
        model = UserModel

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


class SuperUserGroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')


class AdminUserUpdateForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'is_superuser', 'is_staff', 'user_permissions', 'groups')
