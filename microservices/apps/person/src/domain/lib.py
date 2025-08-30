# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from datetime import datetime
import json
from typing import Optional
from link_domain.imdb.base import ImdbHelper
from sqlalchemy.engine.base import Connection
from person.src.models.person_info import (
    PersonInfoCreate,
    PersonInfoRead,
    PersonInfoUpdate,
    PersonInfoResponses,
    PersonInfoResponse
)
from person.src.models.person_saga_state import (
    PersonSagaStateCreate, PersonSagaStateRead, PersonSagaStateUpdate
)
from dateutil import parser


class PersonLib(
    PersonInfoCreate, PersonInfoRead, PersonInfoUpdate,
    PersonInfoResponses, ImdbHelper,
    PersonSagaStateCreate, PersonSagaStateRead, PersonSagaStateUpdate
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def convert_imdb_date(self, val: str) -> Optional[datetime]:
        return parser.parse(val) if val else None
 
    def get_person_info(self, imdbId: str, data: dict) -> dict:

        return dict(
            imdb_id=imdbId,
            name=data.get("name"),
            birth_place=data.get('birth info').get('birth place') if data.get('birth info') else None,
            akas=data.get('akas'),
            filmography=[
                item.getID()
                for item in data.get('filmography').get('actress', [])
            ] + [
                item.getID()
                for item in data.get('filmography').get('actor', [])
            ] if data.get('filmography') else None,
            mini_biography=data.get("mini biography")[0] if data.get('mini biography') else None,
            birth_date=self.convert_imdb_date(data.get('birth date')),
            titles_refs=[
                v.getID()
                for k,v in data.get('titlesRefs').items()
            ] if data.get('titlesRefs') else None,
            head_shot=self.url_clean(data.get('headshot')),
        )

    def person_info_query_redis_load(self, key) -> PersonInfoResponse:
        redis_result = self.person_redis_engine.get(f"person_info_query:{key}")
        if not redis_result:
            return None

        return self.load_from_redis(PersonInfoResponse, redis_result)

    def person_info_query_redis_dump(self, key, response: PersonInfoResponse):
        redis_conv = response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        self.load_to_redis(self.person_redis_engine, f"person_info_query:{key}", redis_conv)
        
    def redis_delete_person_info_keys(self) -> None:
        self.redis_delete_keys_pipe(self.person_redis_engine, [f"person_info_query:*"]).execute()

    def person_saga_redis_update(self, keys: list[bytes]) -> tuple[list, list]:
        return keys, [
            self.person_state_saga_update(self.get_key(key, 2), **json.loads(state))
            for key,state in zip(keys, self.person_redis_engine.mget(keys)) if state
        ]
        
    def person_info_redis_create(self, db: Connection, key_match: str = None, keys: list[str] = None) -> tuple[list, list]:
        keys = self.search_key(self.person_redis_engine, key_match, 1000) if not keys else keys
        if not keys:
            return [],[]
        
        # get completed imdb_ids
        imdb_ids = {self.get_key(k, 2) for k in keys if k is not None}
        all_completed = [k.imdb_id for k in self.find_person_imdb_completed(db, imdb_ids)]
        
        remaining_keys = [
            k for k in keys if k is not None and self.get_key(k, 2) not in all_completed
        ]
        
        if not remaining_keys:
            return [],[]
    
        return remaining_keys, [
            self.person_info_create_imdb(**json.loads(state))
            for key,state in zip(remaining_keys, self.person_redis_engine.mget(remaining_keys))
        ]
