# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_domain.base import LinkDomain
from movie.src.models import MovieModels
from movie.src.models.movie_info import MovieInfoResponse


class MovieLib(LinkDomain, MovieModels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def process_movie_info(self, imdb_id: str) -> dict:
        movie_info = self.imdb_ng_helper.get_movie_by_id(imdb_id)
        return self.imdb_ng_helper.get_movie_info(imdb_id, movie_info)
