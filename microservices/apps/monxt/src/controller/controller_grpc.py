# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
from link_lib.microservice_dynamic_link import MicroserviceDynamicLinkImport
from link_lib.microservice_generic_model import GenericLinkModel

class GrpcController:
    """
    List of the class models for each query type.
    These classes must be in the ../api/grpc/ directory
    """

    @staticmethod
    def handler(topic: str, **kwargs) -> dict:
      registered_topics = [
        "GetRemainingMovieCastQuery",
        "GetShowsQuery",
        "GetShowsSeasonQuery",
        "GetShowsEpisodeQuery",
        "GetAllShowsSeasonQuery",
        "GetCurrentEpisodeQuery",
        "GetRemainingShowsCastQuery",
      ]

      if topic not in registered_topics:
        return dict(message=f"Topic {topic} not found in monxt microservice", received=False)

      return MicroserviceDynamicLinkImport.fork([
        *[f"../../../{ms}/src/api/grpc/" for ms in GenericLinkModel().enabled_microservices]
      ], topic, **kwargs).execute()
