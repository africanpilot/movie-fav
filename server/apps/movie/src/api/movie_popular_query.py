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
        
        limit = pageInfo["first"] if "first" in pageInfo and pageInfo["first"] else 5
        movie_popular_ids = [movie.getID() for movie in lib.get_popular_movies()[:limit]]
        
        redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
        redis_result = redis_db.get("movie_popular_query")
        response = json.loads(redis_result) if redis_result else None        

        if response and response["response"]["code"] == 200 and response["result"]:
            return response 
        else:
            with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                lib.gen.log.debug(f"here")
                response = lib.movie_imdb_response(info=info, db=db, pageInfo=pageInfo, filterInput={"movie_imdb_info_imdb_id": movie_popular_ids}, userId=token_decode["user_id"])               
                
                # can create pipeline if needed
                redis_db.set("movie_popular_query", json.dumps(response), ex=86400) #ex is in secs 86400
                
                return response