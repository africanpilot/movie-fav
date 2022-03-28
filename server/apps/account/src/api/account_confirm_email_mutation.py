# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib

class AccountConfirmEmailMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_confirm_email(self, info: object) -> dict:
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info, email=True)
        if not general_validation_payload["response"]["success"]:
            return general_validation_payload

        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            
            # update user to confirmed email
            sql = lib.update_email_confirmed(ids=token_decode["user_id"])

            # find pattern match for user then delete
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            search = [
                f"""account_me_query:{token_decode["user_id"]}""",
                f"""movie_fav_query:{token_decode["user_id"]}:*"""
            ]
            lib.gen.redis_delete_keys_pipe(redis_db, search).execute()  
            
            return lib.account_response(info=info, db=db, oneQuery=sql, filterInput={"account_info_id": token_decode["user_id"]}) 