# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property
from itertools import zip_longest
import json
from typing import Union
from link_lib.microservice_to_postgres import DbConn
from link_lib.microservice_general import LinkGeneral
from link_config.config import APP_REDIS_EXPIRE
from link_lib.microservice_general import GeneralJSONEncoder
from redis.client import Redis


class LinkRedis(LinkGeneral, DbConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @cached_property
    def default_redis_engine(self) -> Redis:
        return self.get_redis_session("redisdb_default")
    
    @cached_property
    def account_redis_engine(self) -> Redis:
        return self.get_redis_session("redisdb_account")
    
    @cached_property
    def movie_redis_engine(self) -> Redis:
        return self.get_redis_session("redisdb_movie")
    
    @cached_property
    def notifications_redis_engine(self) -> Redis:
        return self.get_redis_session("redisdb_notifications")
    
    @cached_property
    def person_redis_engine(self) -> Redis:
        return self.get_redis_session("redisdb_person")
    
    @cached_property
    def shows_redis_engine(self) -> Redis:
        return self.get_redis_session("redisdb_shows")
    
    def batcher(self, iterable: object, n: int) -> object:
        return zip_longest(*[iter(iterable)] * n)

    def redis_delete_keys_pipe(self, db: Redis, search: Union[str, list], n: int = 50) -> object:
        pipe = db.pipeline()
        if type(search) == str:
            search = [search]

        for item in search:
            for keybatch in self.batcher(db.scan_iter(item), n):
                pipe.delete(*filter(None, keybatch))

        return pipe
    
    def search_key(self, db: Redis, key: str, n: int) -> list:
        result = list(*filter(None, [
            keybatch for keybatch in self.batcher(db.scan_iter(key), n) if keybatch
        ]))
        
        return [i for i in result if i is not None]
           
    def load_to_object(self, responseObject, redis_result):
        return responseObject(**json.loads(redis_result))
    
    def load_from_redis(self, responseObject, redis_result):
        redis_response = responseObject(**json.loads(redis_result))

        if redis_response.response.code == 200 and redis_response.result:
            return redis_response
        
        return None
    
    def load_to_redis(self, db: Redis, key: str, result: dict, ex: int = APP_REDIS_EXPIRE) -> None:
        db.set(key,json.dumps(result, cls=GeneralJSONEncoder), ex=ex)

    def get_key(self, key: bytes, loc: int):
        return key.decode("utf-8").split(":")[loc]
