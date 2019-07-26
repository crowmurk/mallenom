from django.contrib.auth.decorators import permission_required
from django.urls import path, include

from . import views


app_name = 'staffing'

department = [
    path('', views.DepartmentList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.DepartmentCreate.as_view()), name='create'),
    path('<slug:slug>/', views.DepartmentDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', permission_required('is_superuser')(views.DepartmentUpdate.as_view()), name='update'),
    path('<slug:slug>/delete/', permission_required('is_superuser')(views.DepartmentDelete.as_view()), name='delete'),
]

position = [
    path('', views.PositionList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.PositionCreate.as_view()), name='create'),
    path('<slug:slug>/', views.PositionDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', permission_required('is_superuser')(views.PositionUpdate.as_view()), name='update'),
    path('<slug:slug>/delete/', permission_required('is_superuser')(views.PositionDelete.as_view()), name='delete'),
]

staffing = [
    path('', views.StaffingList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.StaffingCreate.as_view()), name='create'),
    path('<int:pk>/', views.StaffingDetail.as_view(), name='detail'),
    path('<int:pk>/update/', permission_required('is_superuser')(views.StaffingUpdate.as_view()), name='update'),
    path('<int:pk>/delete/', permission_required('is_superuser')(views.StaffingDelete.as_view()), name='delete'),
]

urlpatterns = [
    path('department/', include((department, 'department'))),
    path('position/', include((position, 'position'))),
    path('staffing/', include((staffing, 'staffing'))),
]
