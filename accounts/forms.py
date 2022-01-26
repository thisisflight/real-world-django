from django import forms
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       PasswordChangeForm, PasswordResetForm,
                                       SetPasswordForm)

from utils.forms import update_fields_widget
from .models import Profile


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('username', 'password1', 'password2'), 'form-control')


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('username', 'password'), 'form-control')


class ChangeProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('avatar',), 'form-control')


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('old_password', 'new_password1', 'new_password2'), 'form-control')


class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('email',), 'form-control')


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('new_password1', 'new_password2',), 'form-control')
