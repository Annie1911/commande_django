# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserPreference

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, label="Nom d'utilisateur")
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, label="Mot de passe")
    

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['theme', 'language']