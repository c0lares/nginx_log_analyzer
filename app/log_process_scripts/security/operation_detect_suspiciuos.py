from collections import defaultdict
from datetime import datetime, timedelta
import re
from config import REQUESTS_THRESHOLD, ERROR_THERESHOLD, SUSPICIOUS_PATTERNS


def detect_ips_with_lotof_requests(log_processed, time_window=timedelta(minutes=1)):
    ip_access_times = defaultdict(list)
    for log in log_processed:
        ip = log['log_dict']['ip']
        timestamp = datetime.strptime(log['log_dict']['date_time_utc'], '%d/%b/%Y:%H:%M:%S %z')
        ip_access_times[ip].append(timestamp)
        last_date_time = timestamp
    suspicous_ips = []
    for ip, timestamps in ip_access_times.items():
        timestamps.sort()
        for i in range(len(timestamps) - REQUESTS_THRESHOLD + 1):
            if timestamps[i + REQUESTS_THRESHOLD - 1] - timestamps[i] <= time_window:
                suspicous_ips.append(ip)
                break
    if not suspicous_ips:
        return None
    return {
        'suspicous_ips': str(suspicous_ips),
        'last_date_time': str(last_date_time)
    }


def detect_frequent_errors(log_processed):
    error_count = defaultdict(int)
    for log in log_processed:
        status_code = log['log_dict']['requisition_status']
        if int(status_code) >= 400 and int(status_code) <= 599:
            error_count[status_code] += 1
            timestamp = datetime.strptime(log['log_dict']['date_time_utc'], '%d/%b/%Y:%H:%M:%S %z')
            last_date_time = timestamp
    frequent_errors = {code: count for code, count in error_count.items() if count >= ERROR_THERESHOLD}
    if not frequent_errors:
        return None
    return {
        'errors': str(frequent_errors),
        'last_date_time': str(last_date_time)
    }

def detect_logs_with_suspicious_urls(log_processed):
    suspicious_logs = []
    for log in log_processed:
        url = log['log_dict']['url_requested']
        if url is not None:
            for pattern in SUSPICIOUS_PATTERNS:
                if re.search(pattern, url, re.IGNORECASE):
                    suspicious_logs.append(log)
                    timestamp = datetime.strptime(log['log_dict']['date_time_utc'], '%d/%b/%Y:%H:%M:%S %z')
                    last_date_time = timestamp
    if not suspicious_logs:
        return None
    return {
        'suspicious_logs': str(suspicious_logs),
        'last_date_time': str(last_date_time)
    }