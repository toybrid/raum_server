from os import getenv
from .local import *
from dotenv import load_dotenv

load_dotenv()


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': getenv('RAUM_PPROD_DB_NAME'),
    'USER': getenv('RAUM_PPROD_DB_USER'),
    'PASSWORD': getenv('RAUM_PPROD_DB_PASSWORD'),
    'HOST': getenv('RAUM_PPROD_DB_HOST'),
    'PORT': getenv('RAUM_PPROD_DB_PORT'),
    'OPTIONS': {
      'sslmode': 'require',
    },
  }
}