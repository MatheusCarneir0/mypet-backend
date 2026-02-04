<<<<<<< HEAD
=======
# config/settings/development.py
from .base import *

DEBUG = True

# Apenas adiciona apps de desenvolvimento se estiverem instalados
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass

<<<<<<< HEAD
<<<<<<< HEAD
# CORS mais permissivo em desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True
=======
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)
try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
except ImportError:
    pass

INTERNAL_IPS = [
    '127.0.0.1',
]

# Email para console no desenvolvimento
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
<<<<<<< HEAD
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff
=======
>>>>>>> 48d5ddc (Tá funcionando algumas rotas, mas tem erro no login)

