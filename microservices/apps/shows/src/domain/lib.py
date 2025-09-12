# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from typing import Optional

from sqlalchemy.engine.base import Connection
from link_domain.base import LinkDomain
from shows.src.models import ShowsModels
from shows.src.models.shows_info import ShowsInfoResponse
from shows.src.models.shows_episode import ShowsEpisodeResponse


class ShowsLib(LinkDomain, ShowsModels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shows_info_query_redis_load(self, key) -> ShowsInfoResponse:
        redis_result = self.shows_redis_engine.get(f"""shows_info_query:{key}""")
        if not redis_result:
            return None

        return self.load_from_redis(ShowsInfoResponse, redis_result)

    def shows_info_query_redis_dump(self, key, response: ShowsInfoResponse):
        redis_conv = response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        self.load_to_redis(self.shows_redis_engine, f"shows_info_query:{key}", redis_conv)

    def redis_delete_shows_info_keys(self) -> None:
        self.redis_delete_keys_pipe(self.shows_redis_engine, [f"shows_info_query:*"]).execute()

    def shows_episode_query_redis_load(self, key) -> ShowsEpisodeResponse:
        redis_result = self.shows_redis_engine.get(f"""shows_episode_query:{key}""")
        if not redis_result:
            return None

        return self.load_from_redis(ShowsEpisodeResponse, redis_result)
    
    def shows_episode_query_redis_dump(self, key, response: ShowsEpisodeResponse) -> None:
        redis_conv = response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        self.load_to_redis(self.shows_redis_engine, f"shows_episode_query:{key}", redis_conv)
        
    def redis_delete_shows_episode_keys(self) -> None:
        self.redis_delete_keys_pipe(self.shows_redis_engine, [f"shows_episode_query:*"]).execute()

    def shows_saga_redis_update(self, keys: list[bytes]) -> tuple[list, list]:
        return keys, [
            self.shows_state_saga_update(self.get_key(key, 2), **json.loads(state))
            for key,state in zip(keys, self.shows_redis_engine.mget(keys)) if state
        ]

    def process_shows_info(self, imdb_id: str, season: Optional[str] = None, episode: Optional[str] = None) -> dict:
        shows_info = self.imdb_ng_helper.get_shows_by_id(imdb_id, season)
        return self.imdb_ng_helper.get_shows_info(imdb_id, shows_info, season, episode)
