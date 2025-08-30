# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from typing import Optional
from link_lib.microservice_to_grpc_unary_client import UnaryClient


class MovieGrpcClient:
  
  @staticmethod
  def get(topic: str, body: dict):
    return UnaryClient(message=dict(topic=topic, body=body), host="monxt", port=50051).execute()
  
  @staticmethod
  def deserialize_response(response):
    if response.received:
      return dict(message=json.loads(response.message), received=response.received)
    return dict(message=response.message, received=response.received)
  
  @staticmethod
  def get_remaining_movie_cast_query(body: Optional[dict] = None):
    return MovieGrpcClient.deserialize_response(
      MovieGrpcClient.get("GetRemainingMovieCastQuery", body)
    )
    
  @staticmethod
  def get_remaining_movie_downloads_query(body: Optional[dict] = None):
    return MovieGrpcClient.deserialize_response(
      MovieGrpcClient.get("GetRemainingMovieDownloadsQuery", body)
    )
    
  @staticmethod
  def get_movie_downloads_query(body: Optional[dict] = None):
    return MovieGrpcClient.deserialize_response(
      MovieGrpcClient.get("GetMovieDownloadsQuery", body)
    )
