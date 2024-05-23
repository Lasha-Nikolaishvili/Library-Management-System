from datetime import datetime, timedelta


def default_return_date():
    return datetime.now() + timedelta(days=14)


def default_expiration_date():
    return datetime.now() + timedelta(days=1)
