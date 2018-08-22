def validate_and_prep(raw_data, fields):
    def get_value(field):
        try:
            raw_data[field] = raw_data[field].strip()
        finally:
            return raw_data[field] if field in raw_data else None

    clean_values = {}
    for field in fields:
        value = get_value(field)
        if value:
            clean_values[field] = value
    return clean_values
