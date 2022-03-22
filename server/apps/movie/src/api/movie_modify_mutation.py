# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib

class MovieModifyMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def movie_modify_mutation(self, info, movieInput):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            
            movie_id = movieInput["movie_fav_info_id"]
            movieInput.pop("movie_fav_info_id")
            
            # execute sql query
            sql = lib.movie_modify(ids=movie_id, data=movieInput)
            
            return lib.movie_fav_response(info=info, db=db, oneQuery=sql, filterInput={"movie_fav_info_id": movie_id})