import re
from config import logging

#regex
REGEX_DATE = r'(\d+/\d+/\d+ \d+:\d+:\d+)'
REGEX_LOG_LEVEL = r'\[(.*?)\]'
REGEX_PROCESS_ID = r'(\d+#\d+)'
REGEX_CONNECTION_ID = r': (\*\d+)'
REGEX_MESSAGE = r'\d: (\*\d+?)?(.+?)(,|$)'
REGEX_CLIENT = r'client: (\d+\.\d+\.\d+\.\d+)'
REGEX_REQUEST = r'request: "(.+?)"'
REGEX_HOST = r'host: "(.+?)"'
REGEX_SERVER = r'server: .+?(\s|,|$)'


#Functions
output_if_not_none = lambda s: f".{s}" if s is not None else ""

def extract_from_regex(regex, line, number_group):
    match = re.search(regex, line)
    return match.group(number_group) if match else None

def check_priority_error(log_level):
    switcher = {
    'emerg': 7,
    'alert': 6,
    'crit': 5,
    'error': 4,
    'warn': 3,
    'notice': 2,
    'info': 1,
    'debug': 0
    }
    return switcher.get(log_level)
    

def find_information_in_log(line):
    return {
        'date_time': extract_from_regex(REGEX_DATE, line, 1),
        'log_level': extract_from_regex(REGEX_LOG_LEVEL, line, 1),
        'process_id': extract_from_regex(REGEX_PROCESS_ID, line, 1),
        'connection_id': extract_from_regex(REGEX_CONNECTION_ID, line, 1),
        'message': extract_from_regex(REGEX_MESSAGE, line, 2),
        'client': extract_from_regex(REGEX_CLIENT, line, 1),
        'request': extract_from_regex(REGEX_REQUEST, line, 1),
        'host': extract_from_regex(REGEX_HOST, line, 1),
        'server': extract_from_regex(REGEX_SERVER, line, 1)
    }
# Open the log file in read mode

def log_error_process(log_file_path):
    processed_lines = []
    try:
        with open(log_file_path, 'r') as file:
            log_lines = file.readlines()
            for line in log_lines:
                actual_line = line.strip()
                log_dict = find_information_in_log(actual_line)
                log_dict['priority'] = check_priority_error(log_dict['log_level'])
                processed_lines.append({
                'log_error_dict': log_dict
                })
            return processed_lines
    except FileNotFoundError:
        logging.error("O arquivo access.log nao foi encontrado, seguindo para o proximo log")
        return None
    except IOError:
        logging.error("Nao foi possivel ler o arquivo access.log, seguindo para o proximo log")
        return None
    except Exception:
        logging.exception(f"Erro durante a leitura do log,seguindo para o proximo log")
        return None
