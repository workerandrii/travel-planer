from django.urls import path
from . import views

urlpatterns = [
    path('api/projects/', views.project_list_create, name='project-list-create'),
    path('api/projects/<int:pk>/', views.project_detail, name='project-detail'),
    path('api/projects/<int:project_id>/places/', views.project_places_list_create, name='project-places-list-create'),
]