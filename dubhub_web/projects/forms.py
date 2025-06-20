from django import forms
from .models import Projects

class form_project(forms.ModelForm):
    director = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    class Meta:
        model = Projects
        fields = ['title', 'description', 'director']