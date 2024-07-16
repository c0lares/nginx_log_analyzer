from config import LOG_FILE_PATH_ACCESS, LOG_FILE_PATH_ERROR, ACCOUNT_ID_GEOIP, LICENSE_KEY_GEOIP, logging
from db.db_operations import process_all_logs

## Inserindo dados do access.log
process_all_logs(LOG_FILE_PATH_ACCESS, LOG_FILE_PATH_ERROR, ACCOUNT_ID_GEOIP, LICENSE_KEY_GEOIP)