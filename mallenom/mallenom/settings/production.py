from .base import *

from ..log_filters import ManagementFilter

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'localhost',
    '127.0.01',
]

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/lib/mallenomTimeSheet/db.sqlite3',
    }
}

# Logging

verbose = (
    "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(funcName)s [%(message)s]"
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'remove_migration_sql': {
            '()': ManagementFilter,
        },
    },
    'formatters': {
        'verbose': {
            'format': verbose,
            'datefmt': "%Y-%b-%d %H:%M:%S",
        },
    },
    'handlers': {
        'file': {
            'filters': [
                'remove_migration_sql',
            ],
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/httpd/mallenomTimeSheet.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'file',
            ],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Email

# # Сообщения сохраняются в файл
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/var/log/httpd/mallenomTimeSheet.mail'
# Поле 'From' если не указано
DEFAULT_FROM_EMAIL = 'no-reply@mallenom.local'
# Поле 'From' если отправлено ADMINS и MANAGERS
SERVER_EMAIL = 'contact@mallenom.local'
# Префикс темы сообщения
EMAIL_SUBJECT_PREFIX = '[Mallenom  Time Sheet]'
# Поле 'To' если отправлено MANAGERS
MANAGERS = (('Us', 'ourselves@mallenom.local'),)
# Поле 'To' если отправлено ADMINS
ADMINS = (('Admin', 'admin@mallenom.local'),)
