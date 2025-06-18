import os

# პროექტის ძირითადი დირექტორია
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# საიდუმლო გასაღები - შეცვალეთ ეს პროდუქციაში!
SECRET_KEY = 'თქვენი-საიდუმლო-გასაღები-აქ_შეცვალეთ' # !!! მნიშვნელოვანია: შეცვალეთ ეს პროდუქციაში !!!

# დებაგირების რეჟიმი
DEBUG = True # დააყენეთ False პროდუქციაში

# დაშვებული ჰოსტები
ALLOWED_HOSTS = ['*'] # შეზღუდეთ ეს პროდუქციაში

# დაინსტალირებული აპლიკაციები
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken', # ტოკენის აუთენტიფიკაციისთვის
    'drf_yasg',                 # Swagger დოკუმენტაციისთვის
    'django_filters',           # ფილტრაციისთვის
    'core',                     # თქვენი ძირითადი აპლიკაცია
    'users',                    # თქვენი მომხმარებლის აპლიკაცია
    'books',                    # თქვენი წიგნების აპლიკაცია
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'book_exchange_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'book_exchange_api.wsgi.application'

# მონაცემთა ბაზა 
# PostgreSQL-ის გამოყენება Docker-ისთვის, SQLite ადგილობრივი განვითარებისთვის
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db', # ეს ეხება სერვისის სახელს docker-compose.yml-ში
        'PORT': '5432',
    }
}
# SQLite ადგილობრივი განვითარებისთვის (გაააქტიურეთ თუ გსურთ გამოიყენოთ Docker-ის გარეშე)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# პაროლის ვალიდაცია
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token cd6979faf4ced86c6afdb49f0b5797a000000000'
        }
    }
}

# REST Framework პარამეტრები
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication', # Browsable API-ისთვის
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # მხოლოდ წაკითხვის დაშვება არაავტორიზებულებისთვის
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
    # 'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
}

# ლოკალიზაცია
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tbilisi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# სტატიკური ფაილები (Static files)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # collectstatic-ისთვის პროდუქციაში

# მედია ფაილები (Media files) - მომხმარებლის მიერ ატვირთული კონტენტი
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ნაგულისხმევი პირველადი გასაღების ველის ტიპი
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# მორგებული მომხმარებლის მოდელი (Custom User Model) (თუ გადაწყვეტთ Django-ს User-ის გაფართოებას)
AUTH_USER_MODEL = 'users.User' # ან 'core.User' თუ იქ განათავსეთ
