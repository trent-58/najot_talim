from pathlib import Path

from environs import env

env.read_env( ".env" )
BASE_DIR = Path( __file__ ).resolve().parent.parent
SECRET_KEY = env.str( "SECRET_KEY" )
DEBUG = env.bool( "DEBUG", False )
ALLOWED_HOSTS = env.list( "ALLOWED_HOSTS" )

INSTALLED_APPS = [ "corsheaders", "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
                   "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "rest_framework",
                   "rest_framework_simplejwt", "users", "accounts", "finance", 'rest_framework.authtoken']

MIDDLEWARE = [ "django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
               "corsheaders.middleware.CorsMiddleware", "django.middleware.common.CommonMiddleware",
               "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware",
               "django.contrib.messages.middleware.MessageMiddleware",
               "django.middleware.clickjacking.XFrameOptionsMiddleware", ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [ {
  "BACKEND": "django.template.backends.django.DjangoTemplates",
  "DIRS": [ BASE_DIR / "backend/templates" ],
  "APP_DIRS": True,
  "OPTIONS": {
    "context_processors": [ "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages", ],
    },
  }, ]

WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
    },
  }

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "users.auth.BearerTokenAuthentication",
    ],
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
}

AUTH_PASSWORD_VALIDATORS = [ {
  "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
  }, {
  "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
  }, {
  "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
  }, {
  "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
  }, ]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [ BASE_DIR / "static", ]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True
