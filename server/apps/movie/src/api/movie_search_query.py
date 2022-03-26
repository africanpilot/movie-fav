# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
import json

class MovieSearchQuery:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def movie_search_query(self, info, pageInfo, filterInput):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if not general_validation_payload["response"]["success"]:
            return general_validation_payload
        
        # get imdb data based on search title ### TODO: better search method if any ####
        if filterInput["search_type"] == "search_title":
            movies = lib.search_movie_by_title(search=filterInput["search_value"])

            # get movie info limit return
            movie_list = []
            limit = pageInfo["first"] if "first" in pageInfo and pageInfo["first"] else 5
            for i,movie in enumerate(movies):
                movie_payload = lib.get_movie_info(movie.getID(), movie)
                movie_list.append(movie_payload)
                if i+1 == limit:
                    break
            return lib.gen.success_response(result=movie_list, pageInfo={"page_info_count":len(movie_list)})
                
        # get imdb data based on search title
        if filterInput["search_type"] == "search_imdb_id":
            
            # movie_search_info = lib.get_movie_by_id(imdbId=filterInput["search_value"])
            # movie_payload = lib.get_movie_info(filterInput["search_value"], movie_search_info)
            # movie_list.append(movie_payload)
            
            filterData = {"movie_imdb_info_imdb_id": filterInput["search_value"]}
            redis_filter_info = {**pageInfo, **filterData}
            lib.gen.log.debug(f"""movie_search_query:{token_decode["user_id"]}:{redis_filter_info}""")
            
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            redis_result = redis_db.get(f"""movie_search_query:{token_decode["user_id"]}:{redis_filter_info}""")
            response = json.loads(redis_result) if redis_result else None             

            if response and response["response"]["code"] == 200 and response["result"]:
                lib.gen.log.info(f"redis will get data")
                return response 
            else:
                lib.gen.log.info(f"postgres will get data")
            
                with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                    
                    response = lib.movie_imdb_response(info=info, db=db, pageInfo=pageInfo, filterInput=filterData, userId=token_decode["user_id"])
                    # lib.gen.log.debug(f"response: {response}")
                    # can create pipeline if needed
                    redis_db.set(f"""movie_search_query:{token_decode["user_id"]}:{redis_filter_info}""", json.dumps(response), ex=86400) #ex is in secs 86400
                    
                    return response
            
                