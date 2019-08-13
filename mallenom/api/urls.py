from django.urls import path, include

from . import views


app_name = 'api'

employment = [
    path('', views.EmploymentListEmployee.as_view(), name='list'),
]

employee = [
    path('<int:pk>/employment/', include((employment, 'employment'))),
]

urlpatterns = [
    path('employee/', include((employee, 'employee'))),
]
