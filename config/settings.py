from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS = ['*']

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".devtunnels.ms",
    ".vercel.app",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "complaint",
    "core",
    "dashboard",
    "market",
    "membership",
    "axes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'complaint.context_processors.pengaduan_form',
                'dashboard.context_processors.pengaduan_pending_count',
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = 'dashboard:login'
LOGIN_REDIRECT_URL = 'dashboard:home_dashboard'
LOGOUT_REDIRECT_URL = 'dashboard:login'

# Authentication backends (django-axes wajib didaftarkan)
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# django-axes: lockout brute-force login
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1          # jam, otomatis kebuka lagi
AXES_LOCKOUT_PARAMETERS = ["username"]

# Custom admin path (jangan hardcode, ambil dari .env)
ADMIN_PATH = os.getenv("ADMIN_PATH", "admin/")

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Supabase Storage (S3-compatible)
AWS_ACCESS_KEY_ID        = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY    = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME  = os.getenv("AWS_STORAGE_BUCKET_NAME", "media")
AWS_S3_ENDPOINT_URL      = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME       = os.getenv("AWS_S3_REGION_NAME", "ap-southeast-1")
SUPABASE_PROJECT_REF     = os.getenv("SUPABASE_PROJECT_REF")    

AWS_S3_FILE_OVERWRITE    = False
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL          = None       # ← WAJIB: hapus ACL header (Supabase tidak support)
AWS_QUERYSTRING_AUTH     = False      # ← WAJIB: matikan presigned URL

AWS_S3_CUSTOM_DOMAIN = (
    f"{SUPABASE_PROJECT_REF}.supabase.co"
    f"/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"
)

# Semua file media dikelola django-storages
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"