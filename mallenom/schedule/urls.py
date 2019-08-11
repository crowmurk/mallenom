from django.contrib.auth.decorators import permission_required
from django.urls import path, include

from . import views


app_name = 'schedule'

project = [
    path('', views.ProjectList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.ProjectCreate.as_view()), name='create'),
    path('<slug:slug>/', views.ProjectDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', permission_required('is_superuser')(views.ProjectUpdate.as_view()), name='update'),
    path('<slug:slug>/delete/', permission_required('is_superuser')(views.ProjectDelete.as_view()), name='delete'),
]

assignment = [
    path('', views.AssignmentList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.AssignmentCreate.as_view()), name='create'),
    path('<int:pk>/', views.AssignmentDetail.as_view(), name='detail'),
    path('<int:pk>/update/', permission_required('is_superuser')(views.AssignmentUpdate.as_view()), name='update'),
    path('<int:pk>/delete/', permission_required('is_superuser')(views.AssignmentDelete.as_view()), name='delete'),
]

projectassignment = [
    path('', views.ProjectAssignmentList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.ProjectAssignmentCreate.as_view()), name='create'),
    path('<int:pk>/', views.ProjectAssignmentDetail.as_view(), name='detail'),
    path('<int:pk>/update/', permission_required('is_superuser')(views.ProjectAssignmentUpdate.as_view()), name='update'),
    path('<int:pk>/delete/', permission_required('is_superuser')(views.ProjectAssignmentDelete.as_view()), name='delete'),
]

absence = [
    path('', views.AbsenceList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.AbsenceCreate.as_view()), name='create'),
    path('<int:pk>/', views.AbsenceDetail.as_view(), name='detail'),
    path('<int:pk>/update/', permission_required('is_superuser')(views.AbsenceUpdate.as_view()), name='update'),
    path('<int:pk>/delete/', permission_required('is_superuser')(views.AbsenceDelete.as_view()), name='delete'),
]

urlpatterns = [
    path('', include((assignment, 'assignment'))),
    path('project/', include((project, 'project'))),
    path('projectassignment/', include((projectassignment, 'projectassignment'))),
    path('absence/', include((absence, 'absence'))),
]
