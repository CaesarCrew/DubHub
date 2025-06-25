from django.urls import path
from .views import *

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create-project'),
    path('list/', ProjectListView.as_view(), name='list-projects'),
    path('fotos/<str:arquivo>/', FotoProject.as_view(), name='foto-projects'),
    # API endpoints
    path('api/create/', ProjectAPICreateView.as_view(), name='api-create-project'),
    path('api/get/<int:pk>/', ProjectAPIGetView.as_view(), name='api-get-project'),
    path('api/get/all/', ProjectAPIListView.as_view(), name='api-list-projects'),
    path('api/edit/<int:pk>/', ProjectAPIEditView.as_view(), name='api-edit-project'),
    path('api/delete/<int:pk>/', ProjectAPIDeleteView.as_view(), name='api-delete-project'),
]