DEBUG = False
DEVELOPMENT, PRODUCTION = False, True
DEBUG_TOOLBAR = False
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#         'TIMEOUT': 60 * 30,
#         'OPTIONS': {
#             'MAX_ENTRIES': 1500
#         }
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
TEMPLATE_LOADERS = [
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
]
STATIC_URL = 'https://s3-us-west-2.amazonaws.com/static.tstd.today/static/'
WSGI_APPLICATION = 'project.wsgi_prod.application'
ALLOWED_HOSTS = ('*',)