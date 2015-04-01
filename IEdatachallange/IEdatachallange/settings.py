"""
Django settings for IEdatachallange project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)
STATIC_URL =os.path.join(BASE_DIR, "static")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&y)ymp%kwm7iejumq%f%x@+so=@1c4zemd(m!dnivd%t2bbl9_'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hotelapp',
    'mongoengine.django.mongo_auth',
    'djgeojson',
    'geocoder',

    'datetimewidget',
    'django_shell_ipynb',
    'django_extensions',
    'jquery',
    'bootstrap3',
    'rest_framework_mongoengine',
    'rest_framework',
    'django_tables2',
)
#APPEND_SLASH = False
#AUTH_USER_MODEL = 'customauth.MyUser'
AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'main'
USE_L10N = True
USE_TZ = True
USE_I18N = True

# set the mongodb fieldgeneretor for the whole application
#MONGODBFORMS_FIELDGENERATOR = 'hotelapp.fieldgenerator.GeneratorClass'


SERIALIZATION_MODULES = {
    'geojson' : 'djgeojson.serializers'
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)
"""
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'cms.context_processors.media',
)
"""
ROOT_URLCONF = 'IEdatachallange.urls'

WSGI_APPLICATION = 'IEdatachallange.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'



from mongoengine import connect

connect(db="hotelapp", username="hoteladmin", password="hoteladmin");


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS =('static-assets',)


LEAFLET_CONFIG = {


    'SPATIAL_EXTENT':(-3.4492757, 42.9818774, -2.4128145, 43.4568551),

}