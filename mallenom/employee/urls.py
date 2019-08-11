from django.contrib.auth.decorators import permission_required
from django.urls import path, include

from . import views


app_name = 'employee'

employment = [
    path('', views.EmploymentList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.EmploymentCreate.as_view()), name='create'),
    path('<int:pk>/', views.EmploymentDetail.as_view(), name='detail'),
    path('<int:pk>/update/', permission_required('is_superuser')(views.EmploymentUpdate.as_view()), name='update'),
    path('<int:pk>/delete/', permission_required('is_superuser')(views.EmploymentDelete.as_view()), name='delete'),
]

employee = [
    path('', views.EmployeeList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.EmployeeCreate.as_view()), name='create'),
    path('<slug:slug>/', views.EmployeeDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', permission_required('is_superuser')(views.EmployeeUpdate.as_view()), name='update'),
    path('<slug:slug>/delete/', permission_required('is_superuser')(views.EmployeeDelete.as_view()), name='delete'),
]

urlpatterns = [
    path('', include((employment, 'employment'))),
    path('employee/', include((employee, 'employee'))),
]
