# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
import requests
import json

class MoviePopularQuery:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def movie_popular_query(self, info, pageInfo):
        
        lib = Lib()
        movie_list = []
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        redis_filter_info = {**pageInfo}
        lib.gen.log.debug(f"""movie_popular_query:{token_decode["user_id"]}:{redis_filter_info}""")
        
        redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
        redis_result = redis_db.get(f"""movie_popular_query:{token_decode["user_id"]}:{redis_filter_info}""")
        response = json.loads(redis_result) if redis_result else None             

        if response and response["response"]["code"] == 200 and response["result"]:
            lib.gen.log.info(f"redis will get data")
            return response 
        else:
            lib.gen.log.info(f"postgres will get data")
         
            with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        
                response = lib.movie_imdb_response(info=info, db=db, pageInfo=pageInfo, userId=token_decode["user_id"])               
                
                # can create pipeline if needed
                redis_db.set(f"""movie_popular_query:{token_decode["user_id"]}:{redis_filter_info}""", json.dumps(response), ex=86400) #ex is in secs 86400
                
                return response