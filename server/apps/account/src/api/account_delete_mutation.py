# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os

from app_lib.lib import Lib

class AccountDeleteMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_delete(self, info):

        lib = Lib()

        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            
            # execute sql query
            db.execute(lib.account_delete(ids=token_decode["user_id"], db=db))

            # find pattern match for user then delete
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            search = [
                f"""account_me_query:{token_decode["user_id"]}:*""",
                f"""movie_fav_query:{token_decode["user_id"]}:*"""
            ]
            lib.gen.redis_delete_keys_pipe(redis_db, search).execute()  
            
            return lib.gen.success_response(nullPass=True)