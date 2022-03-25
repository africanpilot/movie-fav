# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib

class AccountAuthenticationLogoutMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_authentication_logout(self, info):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            # update user infomation on logout 
            db.execute(lib.update_user_logout_info(ids=token_decode["user_id"]))

            # find pattern match for user then delete
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            search = [
                f"""account_me_query:{token_decode["user_id"]}""",
                f"""movie_fav_query:{token_decode["user_id"]}:*"""
            ]
            lib.gen.redis_delete_keys_pipe(redis_db, search).execute()  
            
            return lib.gen.success_response(nullPass=True, result={})
