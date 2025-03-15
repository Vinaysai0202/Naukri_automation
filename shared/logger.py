import os 
import logging

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(lineno)-4d - %(name)-10s - %(levelname)-8s - %(message)s ',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': '',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename':os.getenv('LOG_FILE', 'app.log'),   
            'level': 'DEBUG',
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'NAUKRILOGGER': {  
            'handlers': ['file'],
            'level': 'INFO',  
            'propagate': False,
        }
    },

}
def setup_logging():
    logging.config.dictConfig(LOGGING)

