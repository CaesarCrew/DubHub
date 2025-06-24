from django import forms
from users.models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'user_type', 'photo']