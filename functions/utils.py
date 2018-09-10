def get_value(raw_data, field):
    try:
        raw_data[field] = raw_data[field].strip()
    finally:
        return raw_data[field] if field in raw_data else None


def validate_and_prep(raw_data, fields):
    clean_values = {}
    for field in fields:
        value = get_value(raw_data, field)
        if value:
            clean_values[field] = value
    return clean_values
