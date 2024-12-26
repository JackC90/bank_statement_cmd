import re
from datetime import datetime
import decimal

# Validations

def validate_date(date_str: str) -> bool:
    """
    Date must be YYYYMMdd format
    """
    if not re.match(r'^\d{8}$', date_str):
        return False
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False
    
def validate_month(date_str: str) -> bool:
    """
    Date must be YYYYMMdd format
    """
    if not re.match(r'^\d{6}$', date_str):
        return False
    try:
        datetime.strptime(date_str, '%Y%m')
        return True
    except ValueError:
        return False

def validate_amount(amount_str: str) -> bool:
    """
    Amount must be greater than zero, decimals are allowed up to 2 decimal places
    """
    try:
        amount = decimal.Decimal(amount_str).quantize(decimal.Decimal('0.01'))
        return amount > 0 and len(str(amount).split('.')[-1]) <= 2
    except ValueError:
        return False
    
def validate_rate(rate_str: str) -> bool:
    """
    Amount must be greater than zero, decimals are allowed up to 2 decimal places
    """
    try:
        amount = decimal.Decimal(rate_str).quantize(decimal.Decimal('0.01'))
        return amount > 0 and amount < 100 and len(str(amount).split('.')[-1]) <= 2
    except ValueError:
        return False