# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from sqlalchemy.sql import text
from colorama import Fore
import json


class AccountMeQuery:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_me(self, info):

        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if not general_validation_payload["response"]["success"]:
            return general_validation_payload
        
        redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
        redis_result = redis_db.get(f"""account_me_query:{token_decode["user_id"]}""")
        response = json.loads(redis_result) if redis_result else None        

        if response and response["response"]["code"] == 200 and response["result"]:
            lib.gen.log.info(f"redis will get data")
            return response 
        else:
            lib.gen.log.info(f"postgres will get data")      
            with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                
                response = lib.account_response(info=info, db=db, filterInput={"account_info_id": token_decode["user_id"]})
                
                # can create pipeline if needed
                redis_db.set(f"""account_me_query:{token_decode["user_id"]}""", json.dumps(response), ex=86400) #ex is in secs 86400
                
                return response