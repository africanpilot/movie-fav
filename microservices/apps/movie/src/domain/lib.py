# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from dateutil import parser
from datetime import datetime
from typing import Optional
from link_domain.imdb import ImdbHelper
from movie.src.models.movie_info import (
    MovieInfoCreate,
    MovieInfoRead,
    MovieInfoUpdate,
    MovieInfoResponses,
    MovieInfoResponse
)

from movie.src.models.movie_saga_state import (
    MovieSagaStateCreate, MovieSagaStateRead, MovieSagaStateUpdate
)
from link_domain.pyratebay import PyratebayLib


class MovieLib(
    MovieInfoCreate, MovieInfoRead, MovieInfoUpdate,
    MovieInfoResponses, ImdbHelper, PyratebayLib,
    MovieSagaStateCreate, MovieSagaStateRead, MovieSagaStateUpdate
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def convert_imdb_date(self, val: str) -> Optional[datetime]:
        if not val:
            return None
        
        try:
            date = parser.parse(val)
            return date
        except Exception:
            pass
        
    
        try:
            date = datetime.strptime(val.split(" (")[0].replace(".",""), '%d %b %Y')
            return date
        except Exception:
            self.log.info(f"Unable to parse date: {val}")
            return None

    def get_movie_info(self, imdbId: str, data: dict) -> dict:
        return dict(
            imdb_id=imdbId,
            title=data.get("title"),
            cast=[item.getID() for item in data.get("cast")] if data.get("cast") else [],
            year=data.get("year"),
            directors=[item["name"] for item in data.get("directors")] if data.get("directors") else [],
            genres=data.get("genres"),
            countries=data.get("countries"),
            plot=data.get("plot")[0] if data.get("plot") else "",
            cover=self.url_clean(data.get("cover")),
            rating=data.get("rating"),
            votes=data.get("votes"),
            run_times=data.get("runtimes"),
            creators=[item.getID() for item in data.get("creators")] if data.get("creators") else [],
            full_cover=data.get("full-size cover url"),
            release_date=self.convert_imdb_date(data.get("original air date")),
            videos=self.get_videos(imdbId),
            download_1080p_url=self.get_magnet_url(data.get("title"), "1080p"),
            download_720p_url=self.get_magnet_url(data.get("title"), "720p"),
            download_480p_url=self.get_magnet_url(data.get("title"), "480p"),
        )

    def movie_info_query_redis_load(self, key) -> MovieInfoResponse:
        redis_result = self.movie_redis_engine.get(f"movie_info_query:{key}")
        if not redis_result:
            return None

        return self.load_from_redis(MovieInfoResponse, redis_result)

    def movie_info_query_redis_dump(self, key, response: MovieInfoResponse):
        redis_conv = response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        self.load_to_redis(self.movie_redis_engine, f"movie_info_query:{key}", redis_conv)
        
    def redis_delete_movie_info_keys(self) -> None:
        self.redis_delete_keys_pipe(self.movie_redis_engine, [f"movie_info_query:*"]).execute()

    def movie_saga_redis_update(self, keys: list[bytes]) -> tuple[list, list]:
        return keys, [
            self.movie_state_saga_update(self.get_key(key, 2), **json.loads(state))
            for key,state in zip(keys, self.movie_redis_engine.mget(keys)) if state
        ]
        
    def movie_info_redis_create(self, key_match: str = None, keys: list[str] = None) -> tuple[list, list]:
        keys = self.search_key(self.movie_redis_engine, key_match, 1000) if not keys else keys
        if not keys:
            return [],[]

        remaining_keys = [k for k in keys if k is not None]

        if not remaining_keys:
            return [],[]
    
        return remaining_keys, [
            self.movie_info_create_imdb(**json.loads(state))
            for key,state in zip(remaining_keys, self.movie_redis_engine.mget(remaining_keys))
        ]
