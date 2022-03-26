# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from json import loads, dumps

class MovieFavQuery:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def movie_fav_query(self, info, pageInfo: dict, filterInput: dict) -> dict:
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if not general_validation_payload["response"]["success"]:
            return general_validation_payload
        
        filterInput.update({"movie_fav_info_user_id": token_decode["user_id"]})
        redis_filter_info = {**pageInfo, **filterInput}
        lib.gen.log.debug(f"""movie_fav_query:{token_decode["user_id"]}:{redis_filter_info}""")
        
        redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
        redis_result = redis_db.get(f"""movie_fav_query:{token_decode["user_id"]}:{redis_filter_info}""")
        response = loads(redis_result) if redis_result else None        

        if response and response["response"]["code"] == 200 and response["result"]:
            lib.gen.log.info(f"redis will get data")
            return response 
        else:
            lib.gen.log.info(f"postgres will get data")
            with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                                
                response = lib.movie_fav_response(info=info, db=db, pageInfo=pageInfo, filterInput=filterInput)

                redis_db.set(f"""movie_fav_query:{token_decode["user_id"]}:{redis_filter_info}""", dumps(response), ex=86400) #ex is in secs 86400
                
                return response