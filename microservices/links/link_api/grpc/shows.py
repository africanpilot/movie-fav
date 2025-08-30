# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from typing import Optional
from link_lib.microservice_to_grpc_unary_client import UnaryClient


class ShowsGrpcClient:
  
  @staticmethod
  def get(topic: str, body: dict):
    return UnaryClient(message=dict(topic=topic, body=body), host="monxt", port=50051).execute()
  
  @staticmethod
  def deserialize_response(response):
    if response.received:
      return dict(message=json.loads(response.message), received=response.received)
    return dict(message=response.message, received=response.received)

  @staticmethod
  def get_shows_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetShowsQuery", body)
    )

  @staticmethod
  def get_shows_season_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetShowsSeasonQuery", body)
    )
    
  @staticmethod
  def get_shows_episode_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetShowsEpisodeQuery", body)
    )
    
  @staticmethod
  def get_all_shows_season_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetAllShowsSeasonQuery", body)
    )
    
  @staticmethod
  def get_current_episode_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetCurrentEpisodeQuery", body)
    )

  @staticmethod
  def get_remaining_shows_cast_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetRemainingShowsCastQuery", body)
    )
    
  @staticmethod
  def get_remaining_shows_downloads_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetRemainingShowsDownloadsQuery", body)
    )

  @staticmethod
  def get_shows_downloads_query(body: Optional[dict] = None):
    return ShowsGrpcClient.deserialize_response(
      ShowsGrpcClient.get("GetShowsDownloadsQuery", body)
    )
