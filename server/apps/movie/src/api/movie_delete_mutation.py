# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib

class MovieDeleteMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def movie_delete_mutation(self, info, movie_fav_info_id):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if not general_validation_payload["response"]["success"]:
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                        
            # execute sql query
            db.execute(lib.movie_delete(db=db, ids=movie_fav_info_id))
            
            # find pattern match for user then delete
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            search = [
                f"""movie_fav_query:{token_decode["user_id"]}:*""",
                f"""movie_search_query:{token_decode["user_id"]}:*"""
            ]
            lib.gen.redis_delete_keys_pipe(redis_db, search).execute()  
            
            return lib.gen.success_response(nullPass=True)