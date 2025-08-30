# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os


def parse_int(v):
    if v is None or v == "":
        return None

    return int(v)

def parse_float(v):
    if v is None or v == "":
        return None

    return float(v)


def str_to_int(v):
    return int(v) if v is not None else v


def parse_boolean(v):
    if v is None:
        return None

    if isinstance(v, bool):
        return v

    if v.lower() in {"f", "false"}:
        return False

    if v.lower() in {"t", "true"}:
        return True

    raise Exception(f"Unrecognized boolean value: {v}")


def parse_list(v, seperator=",", strip=True):
    if v is None:
        return None

    if v:
        items = [i for i in v.split(seperator) if i]
        if strip:
            items = [i.strip() for i in items if i]
        return items

    return []

APP_DEFAULT_ACCESS_KEY = os.getenv("APP_DEFAULT_ACCESS_KEY")
APP_DEFAULT_ENV = os.getenv("APP_DEFAULT_ENV")
LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
assert LOGLEVEL in {
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
}, f"Unrecognized log level: {LOGLEVEL}"
APP_CELERY_BROKER = os.getenv('APP_CELERY_BROKER')
APP_SENDGRID_API_KEY = os.getenv('APP_SENDGRID_API_KEY')
APP_ADDRESS = os.getenv('APP_ADDRESS')
APP_DEFAULT_EMAIL = os.getenv('APP_DEFAULT_EMAIL')
APP_REDIS_EXPIRE = parse_int(os.getenv('APP_REDIS_EXPIRE', 604800))
APP_TOKEN_EXP = parse_int(os.getenv('APP_TOKEN_EXP', 336))
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
NEXT_PUBLIC_PAYMENT_AMOUNT = parse_float(os.getenv('NEXT_PUBLIC_PAYMENT_AMOUNT', 300.00))
NEXT_PUBLIC_PAYMENT_SALES_TAX = parse_float(os.getenv('NEXT_PUBLIC_PAYMENT_SALES_TAX', 0.06))
NEXT_PUBLIC_PAYMENT_STRIPE_SERVICE_PERCENTAGE = parse_float(os.getenv('NEXT_PUBLIC_PAYMENT_STRIPE_SERVICE_PERCENTAGE', 0.029))
NEXT_PUBLIC_PAYMENT_PROVIDER_SERVICE_PERCENTAGE = parse_float(os.getenv('NEXT_PUBLIC_PAYMENT_PROVIDER_SERVICE_PERCENTAGE', 0.010))