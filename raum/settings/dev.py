from os import getenv
from .local import *
from dotenv import load_dotenv

load_dotenv()


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': getenv('RAUM_DEV_DB_NAME'),
    'USER': getenv('RAUM_DEV_DB_USER'),
    'PASSWORD': getenv('RAUM_DEV_DB_PASSWORD'),
    'HOST': getenv('RAUM_DEV_DB_HOST'),
    'PORT': getenv('RAUM_DEV_DB_PORT'),
    'OPTIONS': {
      'sslmode': 'require',
    },
  }
}