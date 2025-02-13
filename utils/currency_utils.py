import re

def clean_currency(value):
    if value is None:
        return 0.0

    value = re.sub(r'[^0-9.,]', '', value)

    if '.' in value and ',' in value:
        value = value.replace('.', '').replace(',', '.')
    elif ',' in value:
        value = value.replace(',', '.')

    try:
        return float(value)
    except ValueError:
        return 0.0
