from .setting.production import *
# from .setting.dev import *

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'arunghosh@gmail.com'
# EMAIL_HOST_PASSWORD = 'hjhj#$'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': '_temp/logs/contact_tree.log',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers':['file'],
#             'propagate': True,
#             'level':'WARNING',
#         },
#         '_main': {
#             'handlers': ['file'],
#             'level': 'WARNING',
#         },
#     }
# }