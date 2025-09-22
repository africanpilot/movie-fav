# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os

from link_lib.microservice_multiprocessing import MicroserviceMultiprocessing

os.chdir(os.path.abspath(os.path.dirname(__file__)))

import link  # noqa: F401

if __name__ == "__main__":
    MicroserviceMultiprocessing(os.getcwd())
