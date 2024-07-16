import logging
from dotenv import dotenv_values


# Carrega todas as variáveis de ambiente do arquivo .env
config = dotenv_values(".env")

####### log_process_scripts
LOG_FILE_PATH_ACCESS = 'nginx_logs/access.log'
LOG_FILE_PATH_ERROR = 'nginx_logs/error.log'
ACCOUNT_ID_GEOIP = config.get('ACCOUNT_ID_GEOIP')
LICENSE_KEY_GEOIP = config.get('LICENSE_KEY_GEOIP')

####### /log_process_scripts/security
REQUESTS_THRESHOLD=3
ERROR_THERESHOLD=3
SUSPICIOUS_PATTERNS=[
    r'/admin',
    r'/login',
    r'SELECT.*FROM',
    r'DELETE\s+FROM',
    r'UPDATE\s+\w+\s+SET',
    r'\' OR \'\d+\'=\'\d+'
]

####### /log_process_scripts/security/email_trigger
EMAIL_SENDER = config.get('EMAIL_SENDER')
EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')
emails_string=config.get('EMAILS_ADMINS')
EMAILS_ADMINS = emails_string.split(',')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Setando o logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")