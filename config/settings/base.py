import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
DEBUG = True

ALLOWED_HOSTS = ['*']
SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'rest_framework',
    'rest_framework.authtoken',

    'v1.users.apps.UsersConfig',
    'v1.openings.apps.OpeningsConfig',
    'v1.tasks.apps.TasksConfig',
    'v1.teams.apps.TeamsConfig',
    'v1.repositories.apps.RepositoriesConfig',
    'v1.videos.apps.VideosConfig',
    'v1.projects.apps.ProjectsConfig',
    'v1.analytics.apps.AnalyticsConfig',
    'v1.feedback.apps.FeedbackConfig',
    'v1.roadmap.apps.RoadmapConfig',
    'v1.app_store.apps.AppStoreConfig',
    'v1.trusted_banks.apps.TrustedBanksConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'thenewboston'),
        'USER': os.getenv('POSTGRES_USER', 'thenewboston'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'thenewboston'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432')
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{os.getenv("REDIS_HOST", "localhost")}:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

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

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CORS_ORIGIN_ALLOW_ALL = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'UPDATE_LAST_LOGIN': True,
    'USER_ID_FIELD': 'uuid',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.backends.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'v1.third_party.rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/day'
    }
}

PAGINATION_DEFAULT_LIMIT = 50
PAGINATION_MAX_LIMIT = 100

SPECTACULAR_SETTINGS = {
    'TITLE': 'thenewboston website API',
    'DESCRIPTION': 'API for thenewboston.com site',
    'VERSION': '0.0.1',
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
CACHE_TTL = 60 * 60  # Cache-Control - 1 hour
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 3600

# S3 setup
AWS_ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET')
AWS_S3_REGION_NAME = os.environ.get('S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
env = os.getenv('ENVIRONMENT')
if env not in ['local', 'postgres_local', 'test']:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
