# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_config.config.base import *

if not APP_CELERY_BROKER:
    raise NameError("APP_CELERY_BROKER must be specified")

if not LOGLEVEL:
    LOGLEVEL = "WARNING"
