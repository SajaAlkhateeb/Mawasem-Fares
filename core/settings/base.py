import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me-before-production")

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "corsheaders",
    "django_filters",
    "anymail",
    # local
    "apps.users",
    "apps.farmers",
    "apps.products",
    "apps.carts",
    "apps.addresses",
    "apps.orders",
    "apps.notifications",
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ---------------------------------------------------------------------------
# Database — SQLite by default; set DATABASE_URL (e.g. Render Postgres) or
# USE_POSTGRES=true + DB_* for PostgreSQL
# ---------------------------------------------------------------------------
if os.environ.get("DATABASE_URL"):
    import dj_database_url

    DATABASES = {"default": dj_database_url.parse(os.environ["DATABASE_URL"])}
elif os.environ.get("USE_POSTGRES", "").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "mawasem"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Cairo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ---------------------------------------------------------------------------
# CORS — allow the dev servers plus the deployed frontend
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://mawsemjo.com",
    "https://www.mawsemjo.com",
] + [o.strip() for o in os.environ.get("CORS_EXTRA_ORIGINS", "").split(",") if o.strip()]

CSRF_TRUSTED_ORIGINS = [
    "https://mawsemjo.com",
    "https://www.mawsemjo.com",
] + [o.strip() for o in os.environ.get("CSRF_EXTRA_ORIGINS", "").split(",") if o.strip()]

# ---------------------------------------------------------------------------
# Email — console backend prints to terminal in development. In production,
# BREVO_API_KEY sends over HTTPS via Brevo (most PaaS hosts, incl. Render,
# block outbound SMTP ports, so raw SMTP won't reach a mail server from
# there); EMAIL_HOST is a fallback for hosts where SMTP ports are allowed.
# ---------------------------------------------------------------------------
if os.environ.get("BREVO_API_KEY"):
    EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
    ANYMAIL = {"BREVO_API_KEY": os.environ["BREVO_API_KEY"]}
elif os.environ.get("EMAIL_HOST"):
    EMAIL_BACKEND       = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST          = os.environ["EMAIL_HOST"]
    EMAIL_PORT          = int(os.environ.get("EMAIL_PORT", "465"))
    EMAIL_USE_SSL        = os.environ.get("EMAIL_USE_SSL", "true").lower() == "true"
    EMAIL_USE_TLS        = os.environ.get("EMAIL_USE_TLS", "false").lower() == "true"
    EMAIL_HOST_USER      = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD  = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_TIMEOUT        = int(os.environ.get("EMAIL_TIMEOUT", "10"))
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "Mawasem <noreply@mawasem.local>")
FRONTEND_URL       = os.environ.get("FRONTEND_URL", "http://localhost:5173")
