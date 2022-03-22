# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
import json

class MovieFavQuery:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def movie_fav_query(self, info, pageInfo, filterInput):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
        redis_result = redis_db.get(f"""movie_fav_query:{token_decode["user_id"]}""")
        response = json.loads(redis_result) if redis_result else None        

        if response and response["response"]["code"] == 200 and response["result"]:
            return response 
        else:
            with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                lib.gen.log.debug(f"here")
                filterInput.update({"movie_fav_info_user_id": token_decode["user_id"]})
                return lib.movie_fav_response(info=info, db=db, pageInfo=pageInfo, filterInput=filterInput)