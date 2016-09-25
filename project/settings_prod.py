DEBUG = False
DEVELOPMENT, PRODUCTION = False, True
DEBUG_TOOLBAR = False
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60 * 30,
        'OPTIONS': {
            'MAX_ENTRIES': 1500
        }
    }
}
TEMPLATE_LOADERS = [
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
]
STATIC_URL = ''
WSGI_APPLICATION = 'project.wsgi_prod.application'
ALLOWED_HOSTS = ()