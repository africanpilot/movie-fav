# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import logging
import logging.config

from link_config import config


class MicroserviceLogger:
    default_log = False
    format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"

    @staticmethod
    def format_gunicorn(name):
        return f"[%(asctime)s] %(levelname)-8s {name} %(message)s"

    @staticmethod
    def format_base(name):
        uvicorn_format = f"[%(asctime)s] %(levelname)-8s {name} %(message)s"
        logging.basicConfig(
            level=getattr(logging, config.LOGLEVEL),
            format=uvicorn_format,
        )
        log = logging.getLogger(name)

        if not MicroserviceLogger.default_log:
            MicroserviceLogger.default_log = log

        return log

    @staticmethod
    def instance(name):
        logging.basicConfig(
            level=getattr(logging, config.LOGLEVEL),
            format=MicroserviceLogger.format,
        )
        log = logging.getLogger(name)

        if not MicroserviceLogger.default_log:
            MicroserviceLogger.default_log = log

        return log


def default_log(show_reject=False):
    log = MicroserviceLogger.default_log
    if log:
        return log
    print("Cannot use default_log() before any logger is initialized!")
    exit(1)
