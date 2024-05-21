from datetime import datetime, timedelta


def default_return_date():
    return datetime.now() + timedelta(days=14)
