try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass

<<<<<<< HEAD
# CORS mais permissivo em desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True
=======
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
>>>>>>> f9a2bae6002ef127bbe409eb0d6089f2507abfff

