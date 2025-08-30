# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import link  # noqa: F401
import logging

from link_lib.microservice_to_grpc_unary_server import UnaryServer
from notifications.src.controller.controller_grpc import GrpcController


if __name__ == '__main__':
  logging.info("Starting unary server")
  UnaryServer.run(GrpcController)
