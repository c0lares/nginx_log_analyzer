from log_process_scripts.log_process_access_scraping import log_process_access
from log_process_scripts.log_process_error_scraping import log_error_process
from log_process_scripts.security.email_trigger import notify_admins
from log_process_scripts.security.security_analyse_logs import check_security
from utils import check_log_processed, generate_log_hash, check_hash_in_database
from .database import *
from datetime import datetime
from config import logging

def process_securiy_info(log_processed):
    try:
        security_dict = check_security(log_processed)
        with db.atomic():
            for logs in security_dict:
                if logs is not None:
                    log_dict_hash = generate_log_hash(logs)
                    if check_hash_in_database(SecurityInform, log_dict_hash) is None:
                        notify_admins(logs)
                        SecurityInform.create(
                            information = logs['mensage'],
                            last_datetime = logs['last_datetime'],
                            hashcode = log_dict_hash
                        )
    except Exception as e:
        logging.exception("Ocorreu um erro na aplicacao: " + str(e))

def process_access_logs(log_file_path, account_id_geoip, license_key_geoip):
    try:
        logging.info("Processando o access.log")
        log_processed = log_process_access(log_file_path, account_id_geoip, license_key_geoip)
        logs_to_check_security = []
        check_log_processed(log_processed)
        with db.atomic():
            for index, logs in enumerate(log_processed):
                logging.info(f"Processando Log {index}")
                log_dict_hash = generate_log_hash(logs['log_dict'])
                if check_hash_in_database(Request, log_dict_hash) is None:
                    logs_to_check_security.append(logs)
                    new_user_agent = UserAgent.create(
                        browser = logs['user_agent_dict']['browser'],
                        browser_version = logs['user_agent_dict']['browser_version'],
                        os = logs['user_agent_dict']['os'],
                        os_version = logs['user_agent_dict']['os_version'],
                        device = logs['user_agent_dict']['device']
                    )
                    new_geo_ip = GeoIp.create(
                        continent_code = logs['geo']['continent_code'],
                        city = logs['geo']['city'],
                        country = logs['geo']['country'],
                        latitude = logs['geo']['latitude'],
                        longitude = logs['geo']['longitude'],
                        time_zone = logs['geo']['time_zone'],
                        state_iso_code = logs['geo']['state_iso_code'],
                        autonomous_system_organization = logs['geo']['autonomous_system_organization'],
                        network = logs['geo']['network']
                    )
                    Request.create(
                        hashcode = log_dict_hash,
                        ip = logs['log_dict']['ip'],
                        date_time_utc = datetime.strptime(logs['log_dict']['date_time_utc'], '%d/%b/%Y:%H:%M:%S %z'),
                        requisition_type = logs['log_dict']['requisition_type'],
                        requisition_status = logs['log_dict']['requisition_status'],
                        requisition_size = logs['log_dict']['requisition_size'],
                        user_agent = new_user_agent,
                        url_requested = logs['log_dict']['url_requested'],
                        geo_ip = new_geo_ip 
                    )
                else:
                    logging.info("Dado ja existe no banco de dados")
            if logs_to_check_security:
               process_securiy_info(logs_to_check_security)
    except Exception as e:
        logging.exception('Error: ' + str(e))

## Inserindo dados do error.log  
def process_error_logs(log_file_path):
    try:
        log_processed = log_error_process(log_file_path)
        
        with db.atomic():
            for index, logs in enumerate(log_processed):
                logging.info(f"Processando log {index} ")
                log_error_dict_hash = generate_log_hash(logs['log_error_dict'])
                if check_hash_in_database(ErrorLog, log_error_dict_hash) is None:
                    ErrorLog.create(
                        date_time = datetime.strptime(logs['log_error_dict']['date_time'], '%Y/%m/%d %H:%M:%S'),
                        log_level = logs['log_error_dict']['log_level'],
                        priority = logs['log_error_dict']['priority'], 
                        process_id = logs['log_error_dict']['process_id'],
                        connection_id = logs['log_error_dict']['connection_id'],
                        message = logs['log_error_dict']['message'],
                        client = logs['log_error_dict']['client'],
                        request = logs['log_error_dict']['request'],
                        host = logs['log_error_dict']['host'],
                        server = logs['log_error_dict']['server'],
                        hashcode = log_error_dict_hash
                    )
                else:
                    logging.info("Dado ja existe no banco de dados")
    except Exception as e:
        logging.exception("Ocorreu um erro na aplicacao: " + str(e))
        
        
def process_all_logs(access_log_file, error_log_file, account_id_geoip, license_key_geoip):
    try:
        db = initialize_database()

        process_access_logs(access_log_file, account_id_geoip, license_key_geoip)
        process_error_logs(error_log_file)

        close_datase(db)
    except Exception as e:
        logging.exception("Ocorreu um erro na aplicacao ao processar todos os logs: " + str(e))
        if db:
            close_datase(db)