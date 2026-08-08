import os
from .settings import *
import dj_database_url
from .settings import BASE_DIR

RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
ALLOWED_HOSTS = [RENDER_HOSTNAME] if RENDER_HOSTNAME else []
CSRF_TRUSTED_ORIGINS = ["https://" + RENDER_HOSTNAME] if RENDER_HOSTNAME else []
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STORAGES = {
    'default':{
        'BACKEND' : 'django.core.files.storage.FileSystemStorage'
    },
    'staticfiles' : {
        'BACKEND' : 'whitenoise.storage.CompressedStaticFilesStorage'
    },
}

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}