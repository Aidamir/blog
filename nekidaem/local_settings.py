import os
from .settings import BASE_DIR
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nekidaem',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

#STATIC_URL = '/static/'
#MEDIA_URL = '/media/'

#STATIC_ROOT=os.path.join(BASE_DIR, 'static')
#MEDIA_ROOT=os.path.join(BASE_DIR, 'static/media')
