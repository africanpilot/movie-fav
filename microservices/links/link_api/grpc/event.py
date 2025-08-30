# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from typing import Optional
from link_lib.microservice_to_grpc_unary_client import UnaryClient


class EventGrpcClient:
  
  @staticmethod
  def get(topic: str, body: dict):
    return UnaryClient(message=dict(topic=topic, body=body), host="monxt", port=50051).execute()
  
  @staticmethod
  def deserialize_response(response):
    if response.received:
      return dict(message=json.loads(response.message), received=response.received)
    return dict(message=response.message, received=response.received)
  
  @staticmethod
  def event_ticket_query(body: Optional[dict] = None):
    return EventGrpcClient.deserialize_response(
      EventGrpcClient.get("EventTicketQuery", body)
    )
