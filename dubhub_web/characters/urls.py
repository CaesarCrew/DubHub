from django.urls import path
from .views import CharacterCreateView, CharacterListView, CharacterDeleteView

urlpatterns = [
    path('create/', CharacterCreateView.as_view(), name='create-character'),
    path('list/', CharacterListView.as_view(), name='list-characters'),
    path('delete/<int:pk>/', CharacterDeleteView.as_view(), name='delete-character'),
]