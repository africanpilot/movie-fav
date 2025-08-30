# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from typing import Optional
from link_lib.microservice_to_grpc_unary_client import UnaryClient


class CartGrpcClient:
  
  @staticmethod
  def get(topic: str, body: dict):
    return UnaryClient(message=dict(topic=topic, body=body), host="monxt", port=50051).execute()
  
  @staticmethod
  def deserialize_response(response):
    if response.received:
      return dict(message=json.loads(response.message), received=response.received)
    return dict(message=response.message, received=response.received)
  
  @staticmethod
  def cart_product_query(body: Optional[dict] = None):
    return CartGrpcClient.deserialize_response(
      CartGrpcClient.get("CartProductQuery", body)
    )
    
  @staticmethod
  def cart_event_query(body: Optional[dict] = None):
    return CartGrpcClient.deserialize_response(
      CartGrpcClient.get("CartEventQuery", body)
    )
