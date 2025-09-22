# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from account.src.app_lib.config.base import *

if not APP_CELERY_BROKER:
    raise NameError("APP_CELERY_BROKER must be specified")

if not LOGLEVEL:
    LOGLEVEL = "WARNING"
