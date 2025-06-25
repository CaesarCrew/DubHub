from django import forms
from django.forms import modelformset_factory
from .models import News, NewsMedia

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']

NewsMediaFormSet = modelformset_factory(
    NewsMedia,
    fields=('file', 'caption', 'news_type'),
    extra=2, 
    can_delete=True
)