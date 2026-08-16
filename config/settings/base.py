from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)

environ.Env.read_env(BASE_DIR / ".env")


# Core

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"],
)


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "allauth",
    "allauth.account",
    "auth_kit",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.users.apps.UsersConfig",
    "apps.students.apps.StudentsConfig",
    "apps.teachers.apps.TeachersConfig",
    "apps.parents.apps.ParentsConfig",
    "apps.academics.apps.AcademicsConfig",
    "apps.communications.apps.CommunicationsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": ("django.template.backends.django." "DjangoTemplates"),
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                ("django.template.context_processors." "request"),
                ("django.contrib.auth.context_processors." "auth"),
                ("django.contrib.messages.context_processors." "messages"),
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": env.db("DATABASE_URL"),
}

DATABASES["default"]["CONN_MAX_AGE"] = 60
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True
DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True


# Redis cache

CACHES = {
    "default": {
        "BACKEND": ("django.core.cache.backends.redis." "RedisCache"),
        "LOCATION": env("REDIS_URL"),
        "KEY_PREFIX": "academe",
        "TIMEOUT": 300,
    }
}


SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

SESSION_COOKIE_NAME = "academe_session"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = "Lax"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "NumericPasswordValidator"),
    },
]


AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"

USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:5173"],
)

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["http://localhost:5173"],
)

CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"

CSRF_FAILURE_VIEW = "apps.core.csrf.csrf_failure"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        ("apps.users.authentication.backends." "CSRFProtectedJWTCookieAuthentication"),
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "auth_kit": "10/minute",
        "user-registration": "20/hour",
    },
    "EXCEPTION_HANDLER": ("apps.core.exceptions.api_exception_handler"),
    "DEFAULT_FILTER_BACKENDS": [
        ("django_filters.rest_framework." "DjangoFilterBackend"),
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": ("rest_framework.pagination." "PageNumberPagination"),
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": ("drf_spectacular.openapi.AutoSchema"),
}


AUTH_KIT = {
    "AUTH_TYPE": "jwt",
    "USE_AUTH_COOKIE": True,
    "SESSION_LOGIN": False,
    "AUTH_COOKIE_SECURE": not DEBUG,
    "AUTH_COOKIE_HTTPONLY": True,
    "AUTH_COOKIE_SAMESITE": env(
        "AUTH_COOKIE_SAMESITE",
        default="Lax",
    ),
    "AUTH_COOKIE_DOMAIN": env(
        "AUTH_COOKIE_DOMAIN",
        default=None,
    ),
    "AUTH_JWT_COOKIE_NAME": "academe_access",
    "AUTH_JWT_COOKIE_PATH": "/",
    "AUTH_JWT_REFRESH_COOKIE_NAME": "academe_refresh",
    "AUTH_JWT_REFRESH_COOKIE_PATH": "/api/v1/auth/",
    "LOGIN_VIEW": ("apps.users.authentication.views." "CSRFProtectedLoginView"),
    "JWT_REFRESH_VIEW": ("apps.users.authentication.views." "CSRFProtectedRefreshView"),
    "USER_SERIALIZER": ("apps.users.authentication.serializers." "AuthUserSerializer"),
    # Accounts are created only by administrators.
    "EXCLUDED_URL_NAMES": [
        "rest_register",
        "rest_verify_email",
        "rest_resend_email",
    ],
    "PASSWORD_RESET_PREVENT_ENUMERATION": True,
}


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"

ACCOUNT_LOGIN_METHODS = {"email"}

ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*",
]

ACCOUNT_EMAIL_VERIFICATION = "none"


SPECTACULAR_SETTINGS = {
    "TITLE": "Academe.io API",
    "DESCRIPTION": "School management API",
    "VERSION": "1.0.0",
}
