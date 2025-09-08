# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_domain.base import LinkDomain
from person.src.models.person_info import PersonInfoResponse
from person.src.models import PersonModels
from dateutil import parser


class PersonLib(LinkDomain, PersonModels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        
    def process_person_info(self, imdb_id: str) -> dict:
        person_info = self.imdb_helper.get_person_by_id(imdb_id)
        return self.imdb_helper.get_person_info(imdb_id, person_info)
