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
        if general_validation_payload != "success":
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                        
            # execute sql query
            db.execute(lib.movie_delete(db=db, ids=movie_fav_info_id))
            
            return lib.gen.success_response(nullPass=True)