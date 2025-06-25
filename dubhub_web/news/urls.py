from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('create/', login_required(NewsCreateView.as_view(), login_url=''), name='create-news'),
    path('delete/<int:pk>/', login_required(NewsDeleteView.as_view(), login_url=''), name='delete-news'),
    path('update/<int:pk>/', login_required(NewsUpdateView.as_view(), login_url=''), name='update-news'),
    path('list/', NewsListView.as_view(), name='list-news'),

    path('api/create/', NewsAPICreateView.as_view(), name='api-create-news'),
    path('api/list/', NewsAPIListView.as_view(), name='api-list-news'),
    path('api/update/<int:pk>/', NewsAPIUpdateView.as_view(), name='api-update-news'),
    path('api/delete/<int:pk>/', NewsAPIDeleteView.as_view(), name='api-delete-news'),
    path('api/get/<int:pk>/', NewsAPIGetView.as_view(), name='api-get-news'),
]