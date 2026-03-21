import re
from datetime import date, datetime

def validate_phone(phone: str) -> bool:
    """Valida formato de teléfono: 229-133-9124"""
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    return bool(re.match(pattern, phone))

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_future_date(date_to_check: date) -> bool:
    """Verifica que una fecha no sea pasada"""
    return date_to_check >= date.today()

def validate_time_format(time_str: str) -> bool:
    """Valida formato de hora: HH:MM"""
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

def validate_time_range(start: str, end: str) -> bool:
    """Verifica que hora_inicio < hora_fin"""
    start_hour = int(start.split(':')[0])
    end_hour = int(end.split(':')[0])
    return start_hour < end_hour