from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.ReportDownload.as_view(), name='report'),
]
