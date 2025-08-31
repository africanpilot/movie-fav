# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import logging
import os

from link_lib.microservice_logger import MicroserviceLogger


def microservice_name():
    """
    Discover the name of the Microservice based on source code directory we're running from.
    """
    cwd = os.getcwd() + "/../.."
    abs = os.path.abspath(cwd)
    return os.path.basename(abs)


class GenericLinkModel:
    def __init__(self):
        self.name: str = microservice_name()
        self.log: logging = MicroserviceLogger.format_base(self.name)
        self.enabled_microservices = [
            "account",
            "movie",
            "notifications",
            "person",
            "shows",
        ]

class GenericModel:
    def __init__(self):
        self.name: str = microservice_name()
        self.log: logging = MicroserviceLogger.format_base(self.name)
