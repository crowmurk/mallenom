import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Loading secret key

SECRET_KEY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'secret.key',
)

SECRET_KEY = open(SECRET_KEY_FILE).read().strip()

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'django_tables2',
    'django_filters',
    'import_export',
    'rangefilter',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'staffing.apps.StaffingConfig',
    'employee.apps.EmployeeConfig',
    'schedule.apps.ScheduleConfig',
    'workcal.apps.WorkCalConfig',
    'reports.apps.ReportsConfig',
    'api.apps.ApiConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware to use

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'global_login_required.GlobalLoginRequiredMiddleware',
]

ROOT_URLCONF = 'mallenom.urls'

# Template engines

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mallenom.wsgi.application'

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Login
LOGIN_REDIRECT_URL = '/'

# All but this views are login requred
PUBLIC_VIEWS = [
    'django.contrib.auth.views.LoginView',
]

# All but this paths are login requred
PUBLIC_PATHS = [
    r'^/i18n/setlang',
]

# Internationalization

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Admin config

ADMIN_SITE_HEADER = _("Mallenom administration")

ADMIN_SITE_TITLE = _("Mallenom site admin")

ADMIN_INDEX_TITLE = _('Site administration')

# Float tolerance
FLOAT_TOLERANCE = 7

# Work day length in hours
WORK_DAY_HOURS = 8
