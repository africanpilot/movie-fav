# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
from link_lib.microservice_dynamic_link import MicroserviceDynamicLinkImport

class GrpcController:
    """
    List of the class models for each query type.
    These classes must be in the ../api/grpc/ directory
    """

    @staticmethod
    def handler(topic: str, **kwargs) -> dict:
      registered_topics = []

      if topic not in registered_topics:
        return dict(message=f"Topic {topic} not found in person microservice", received=False)
      
      return MicroserviceDynamicLinkImport.fork(["../api/grpc/"], topic, **kwargs).execute()
