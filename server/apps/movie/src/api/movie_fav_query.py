# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib

class MovieFavQuery:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def movie_fav_query(self, info, pageInfo, filterInput):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            filterInput.update({"movie_fav_info_user_id": token_decode["user_id"]})
            return lib.movie_fav_response(info=info, db=db, pageInfo=pageInfo, filterInput=filterInput)