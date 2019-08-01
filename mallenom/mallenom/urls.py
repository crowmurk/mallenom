"""mallenom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, register_converter
from django.conf import settings
from django.views.generic import TemplateView, RedirectView

from core.converters import RussianSlugConverter

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

register_converter(RussianSlugConverter, 'slug')

urlpatterns = [
    path('', RedirectView.as_view(
        pattern_name='schedule:assignment:list',
        permanent=False)),
    path('staffing/', include('staffing.urls')),
    path('employee/', include('employee.urls')),
    path('schedule/', include('schedule.urls')),
    path('underconstruction/', TemplateView.as_view(
        template_name='site/underconstruction.html'),
        name='underconstruction'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

# Подключение django debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
