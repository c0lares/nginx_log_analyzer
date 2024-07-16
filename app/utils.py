import json
import hashlib
from ipaddress import IPv4Network
from config import logging

def check_log_processed(log_processed):
    if log_processed is None:
        raise Exception()
    
def custom_serializer(obj):
    if isinstance(obj, IPv4Network):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
    
def generate_log_hash(log_dict):
    log_string = json.dumps(log_dict, sort_keys=True, default=custom_serializer)
    return hashlib.md5(log_string.encode()).hexdigest()

def check_hash_in_database(the_class, log_hash):
    return the_class.get_or_none(hashcode=log_hash)
