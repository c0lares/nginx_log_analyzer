import re
import geoip2.webservice
import ua_parser.user_agent_parser
from geoip2.errors import AddressNotFoundError, AuthenticationError, OutOfQueriesError
from config import logging

#regex
REGEX_DATE = r'\[(.*?)\]'
REGEX_IP_V4 = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) -'
REGEX_IP_V6 = r'(\w+:\w+::\w+)'
REGEX_REQUISITION_TYPE = r'"(\w+ /.+?)"'
REGEX_REQUISITION_STATUS = r'" (\d{3})'
REGEX_REQUISITION_SIZE = r'(\d+) "'
REGEX_USER_AGENT = r'".*?" "(.*?)"'
REGEX_URL_REQUEST = r'\d "(.*?)" ".*?"'

#Functions
output_if_not_none = lambda s: f".{s}" if s is not None else ""

def extract_from_regex(regex, line):
    match = re.search(regex, line)
    return match.group(1) if match else None
    

def find_information_in_log(line):
    return {
        'date_time_utc': extract_from_regex(REGEX_DATE, line),
        'ip': (
            extract_from_regex(REGEX_IP_V4, line) 
            if extract_from_regex(REGEX_IP_V4, line) 
            else extract_from_regex(REGEX_IP_V6, line)),
        'requisition_type': extract_from_regex(REGEX_REQUISITION_TYPE, line),
        'requisition_status': extract_from_regex(REGEX_REQUISITION_STATUS, line),
        'requisition_size': extract_from_regex(REGEX_REQUISITION_SIZE, line),
        'user_agent': extract_from_regex(REGEX_USER_AGENT, line),
        'url_requested': extract_from_regex(REGEX_URL_REQUEST, line)
    }


def parse_user_agent(user_agent):
    parsed_user_agent = ua_parser.user_agent_parser.Parse(user_agent)
    return{
        'browser': parsed_user_agent['user_agent']['family'],
        'browser_version': (
            parsed_user_agent['user_agent']['major'] +
            output_if_not_none(parsed_user_agent['user_agent']['minor']) +
            output_if_not_none(parsed_user_agent['user_agent']['patch'])
        ) if parsed_user_agent['user_agent']['major'] is not None else None,
        'os': parsed_user_agent['os']['family'],
        'os_version': (
            parsed_user_agent['os']['major'] + 
            output_if_not_none(parsed_user_agent['os']['minor']) + 
            output_if_not_none(parsed_user_agent['os']['patch'])
        ) if parsed_user_agent['os']['major'] is not None else None,
        'device': parsed_user_agent['device']['family']
    }

def get_locate_ip(ip, account_id_geoip, license_key_geoip):
    try:
        with geoip2.webservice.Client(account_id_geoip, license_key_geoip, host='geolite.info') as client:
            logging.info(f"Ip {ip} sendo analizado pelo GeoIp")
            response = client.city(ip)
            return {
                'continent_code': response.continent.code,
                'city': response.city.name,
                'country': response.country.name,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude,
                'time_zone': response.location.time_zone,
                'state_iso_code': response.subdivisions.most_specific.iso_code,
                'autonomous_system_organization': response.traits.autonomous_system_organization,
                'network': response.traits.network
            }
    except AddressNotFoundError as e:
        logging.warning("Ip nao encontrado: " + str(e))
        return{
            'continent_code': None,
            'city': None,
            'country': None,
            'latitude': None,
            'longitude': None,
            'time_zone': None,
            'state_iso_code': None,
            'autonomous_system_organization': None,
            'network': None
        }
    except AuthenticationError as e:
        logging.critical("Nao foi possivel autenticar no geoip2")
        raise Exception()
    except OutOfQueriesError as e:
        logging.critical("LImite de querys por dia do geoip2 excedido")
        return{
            'continent_code': None,
            'city': None,
            'country': None,
            'latitude': None,
            'longitude': None,
            'time_zone': None,
            'state_iso_code': None,
            'autonomous_system_organization': None,
            'network': None
        }
    except Exception as e:
        logging.exception("Exception: " + str(e))
        return{
            'continent_code': None,
            'city': None,
            'country': None,
            'latitude': None,
            'longitude': None,
            'time_zone': None,
            'state_iso_code': None,
            'autonomous_system_organization': None,
            'network': None
        }


# Open the log file in read mode

def log_process_access(log_file_path,account_id_geoip, license_key_geoip):
    processed_lines = []
    try:
        with open(log_file_path, 'r') as file:
            # Read all lines of the file into a list
            log_lines = file.readlines()

            # Display or process each line
            for line in log_lines:
                actual_line = line.strip()
                log_dict = find_information_in_log(actual_line)
                user_agent_dict = parse_user_agent(log_dict['user_agent']) if log_dict['user_agent'] is not None else None
                geo_dict = get_locate_ip(log_dict['ip'], account_id_geoip, license_key_geoip) if log_dict['ip'] is not None else None
                processed_lines.append({
                    'log_dict': log_dict,
                    'user_agent_dict': user_agent_dict,
                    'geo': geo_dict
                })
            # exit()
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
