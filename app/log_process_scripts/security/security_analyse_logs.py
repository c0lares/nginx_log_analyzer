from .operation_detect_suspiciuos import detect_ips_with_lotof_requests, detect_frequent_errors, detect_logs_with_suspicious_urls
from config import logging
from datetime import datetime

def check_ips_lotof_requests(log_processed):
    suspicious_ips = detect_ips_with_lotof_requests(log_processed)
    if suspicious_ips is not None:
        logging.critical("Ips suspeitos de cordenar ataques(muitas requisicoes em um intervalo de um minuto): " + suspicious_ips['suspicous_ips'])
        logging.info("Mandando email em relacao ao problema para o administrador cadastrado do sistema")
        report = {
            'mensage': f"Ips suspeitos de cordenar ataques(muitas requisicoes em um intervalo de um minuto): {suspicious_ips['suspicous_ips']}",
            'last_datetime': suspicious_ips['last_date_time'],
            'mesage_to_report': "Ip(s) com muitas requisicoes em 1 minuto"
        }
        return report
    else:
        logging.info("Security ok")
        return None
        
def check_frequent_errors(log_processed):
    errors = detect_frequent_errors(log_processed)
    if errors is not None:
        logging.critical("Muitos errors consecutivos, http_status: " + errors['errors'])
        logging.info("Mandando email em relacao ao problema para o administrador cadastrado do sistema")
        report = {
            'mensage': f"Muitos errors consecutivos, http_status: {errors['errors']}",
            'last_datetime': errors['last_date_time'],
            'mesage_to_report': "Estao ocorrendo erros frequentes"
        }
        return report
    else:
        logging.info("Security ok")
        return None
        
def check_logs_with_suspicious_urls(log_processed):
    suspicious_logs = detect_logs_with_suspicious_urls(log_processed)
    if suspicious_logs is not None:
        logging.critical("Acessos suspeitos pelo seguintes logs: " + suspicious_logs['suspicious_logs'])
        logging.info("Mandando email em relacao ao problema para o administrador cadastrado do sistema")
        now = datetime.now()
        report = {
            'mensage': f"Acessos suspeitos pelo seguintes logs:  {suspicious_logs['suspicious_logs']}",
            'last_datetime': suspicious_logs['last_date_time'],
            'mesage_to_report': "Tentativa(s) de acesso(s) em uma ou mais urls suspeitas "
        }
        return report
    else:
        logging.info("Security ok")
        return None



def check_security(log_processed):
    return[
        check_ips_lotof_requests(log_processed), 
        check_frequent_errors(log_processed),
        check_logs_with_suspicious_urls(log_processed)
    ]
