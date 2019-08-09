from django.contrib.auth.decorators import permission_required
from django.urls import path, include

from . import views


app_name = 'workcal'

day_type = [
    path('', views.DayTypeList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.DayTypeCreate.as_view()), name='create'),
    path('<slug:slug>/', views.DayTypeDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', permission_required('is_superuser')(views.DayTypeUpdate.as_view()), name='update'),
    path('<slug:slug>/delete/', permission_required('is_superuser')(views.DayTypeDelete.as_view()), name='delete'),
]

day = [
    path('', views.DayList.as_view(), name='list'),
    path('create/', permission_required('is_superuser')(views.DayCreate.as_view()), name='create'),
    path('<slug:slug>/', views.DayDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', permission_required('is_superuser')(views.DayUpdate.as_view()), name='update'),
    path('<slug:slug>/delete/', permission_required('is_superuser')(views.DayDelete.as_view()), name='delete'),
]

calendar = [
    path('', views.CalendarDetail.as_view(), name='current'),
    path('<int:year>/', views.CalendarDetail.as_view(), name='year'),
    path('upload/', views.CalendarUpload.as_view(), name='upload'),
]

urlpatterns = [
    path('daytype/', include((day_type, 'daytype'))),
    path('day/', include((day, 'day'))),
    path('calendar/', include((calendar, 'calendar'))),
]
