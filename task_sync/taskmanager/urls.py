from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('projects/<int:project_id>/documents/upload/', views.document_upload, name='document_upload'),
    path('projects/<int:project_id>/collaborators/add/', views.add_collaborator, name='add_collaborator'),
    path('projects/<int:project_id>/collaborators/<int:collaborator_id>/edit/',
        views.edit_collaborator, name='edit_collaborator'),
    path('notifications/', views.notifications_view, name='notifications'),
]