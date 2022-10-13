import os # работа с Операционной системой
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'file':{
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default_formatter',
            'filename': 'bot.log',
            'maxBytes': 1024,
            'backupCount': 3,
        }
    },

    'loggers': {
        'my_logger': {
            'handlers': ['stream_handler', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# Создайте Logger
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_logger')

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = str(os.getenv('BOT_TOKEN'))


admin_id = str(os.getenv('ID_ADMIN')).split(',')


teacher = 448768892

stiker_id = {
    'start_stiker' : 'CAACAgIAAxkBAAEEjcNiZiMoSTQ4-OE5I0imypxWbNTEygACxxgAArfUeElKxssIBSHQXiQE',
    'help_stiker' : 'CAACAgIAAxkBAAEEjcViZiXBB_Qm6YVxwB7o5aO26sEeTwAC_BQAArLFeEnpVEZYfRxtfiQE'
}