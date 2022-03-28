# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from datetime import datetime

class AccountModifyMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_modify(_, info: object, accountModifyInput: dict) -> dict:
        
        lib = Lib()
        
        email = True if "account_info_password" in accountModifyInput and accountModifyInput["account_info_password"] else False
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info,email=email)
        if not general_validation_payload["response"]["success"]:
            return general_validation_payload
        
        # verify password regex
        if "account_info_password" in accountModifyInput and accountModifyInput["account_info_password"]:
            
            # check reTypePasswordMatches
            if accountModifyInput["account_info_password"] and "account_info_password_retype" not in accountModifyInput:
                return lib.gen.http_401_unauthorized_response(msg="Invalid password retype")
            
            if accountModifyInput["account_info_password"] != accountModifyInput["account_info_password_retype"]:
                return lib.gen.http_401_unauthorized_response(msg="Invalid password retype")

            # check password length and hash
            if len(accountModifyInput["account_info_password"]) > 64 or len(accountModifyInput["account_info_password"]) < 8:
                return lib.gen.http_401_unauthorized_response(msg="Invalid password legnth")
            
            if not lib.gen.password_check(password=accountModifyInput["account_info_password"]):
                return lib.gen.http_401_unauthorized_response(msg="Invalid password")
           
            hashed_pw = {"account_info_password":lib.gen.hash_password(accountModifyInput["account_info_password"]).decode("utf-8")}
            accountModifyInput.update(hashed_pw)
            accountModifyInput.pop("account_info_password_retype")
                
        # convert dates
        if "account_contact_birthday" in accountModifyInput and accountModifyInput["account_contact_birthday"]:
            date_convert = {"account_contact_birthday":str(datetime.strptime(accountModifyInput["account_contact_birthday"],'%Y-%m-%d %H:%M:%S.%f'))}
            accountModifyInput.update(date_convert)

        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            
            # check password change expire time
            exp_date = lib.get_password_expire_date(db=db, ids=token_decode["user_id"])["account_info_forgot_password_expire_date"]
            if exp_date < datetime.utcnow():
                return lib.gen.http_401_unauthorized_response(msg="Please confirm forgot password email") 
         
            # execute sql query
            sql = lib.account_modify(id=token_decode["user_id"], data=accountModifyInput)  
            response = lib.account_response(info=info, db=db, oneQuery=sql, filterInput={"account_info_id": token_decode["user_id"]})
            
            # find pattern match for user then delete
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            lib.gen.redis_delete_keys_pipe(redis_db, f"""account_me_query:{token_decode["user_id"]}""").execute()      
            
            return response