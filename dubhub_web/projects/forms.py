from django import forms
from .models import Projects

class form_project(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['created_at', 'director']