# Cloudinary configuration
import cloudinary
import cloudinary.uploader
import cloudinary.api


from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
# DEBUG = os.getenv("DEBUG", "False") == "True"D
DEBUG=True
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    # "daphne",   # ASGI server
    "channels",
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'food99api',
]
# ASGI_APPLICATION = "food99api.asgi.application"

# Tell Django to use the custom user model
AUTH_USER_MODEL = 'food99api.CustomUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "food99api.middleware.DisableCSRFMiddleware",  # add here
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),   # default: 5 minutes
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),     # default: 1 day
    "ROTATE_REFRESH_TOKENS": False,                   # set True if you want new refresh token each time
    "BLACKLIST_AFTER_ROTATION": True,                 # requires blacklist app
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
DATABASES = {    
    "default": {},   # will be assigned below

    "local": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "local_db",
        "USER": "local_user",
        "PASSWORD": "local_pass",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
    
    "remote": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.zbcwxsihcukcnaxuxodl',
        'PASSWORD': 'akshatgupta5555',
        'HOST': 'aws-1-ap-south-1.pooler.supabase.com',
        'PORT': '6543',
    }
}

import socket

def can_connect(host, port, timeout=2):
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except:
        return False

REMOTE_HOST = DATABASES["remote"]["HOST"]
REMOTE_PORT = DATABASES["remote"]["PORT"]

if can_connect(REMOTE_HOST, REMOTE_PORT):
    print("📡 Using Remote Database (Supabase)")
    DATABASES["default"] = DATABASES["remote"]
else:
    print("💾 Remote not reachable → Using Local Database")
    DATABASES["default"] = DATABASES["local"]


# Media storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dbe8vybbp',
    'API_KEY': '949178684912937',
    'API_SECRET': 'aIknh9wAy6uRaCE_uA6J8uMGpoY',
}
# CASHFREE_APP_ID='TEST10780741c8ed77d4335970bc544314708701'
# CASHFREE_SECRET_KEY='cfsk_ma_test_8469dc1fc0f34e541aab6b56c4bd3842_9b7b3ff5'
CASHFREE_APP_ID = os.environ.get('CASHFREE_APP_ID')
CASHFREE_SECRET_KEY = os.environ.get('CASHFREE_SECRET_KEY')
CASHFREE_API_URL = 'https://api.cashfree.com/pg'

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
