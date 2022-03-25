# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from sqlalchemy.sql import text
from colorama import Fore

class AccountAuthenticationLoginMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_authentication_login(self, info, accountLoginInput):

        lib = Lib()
        
        # get service name
        service_name = lib.gen.get_service_from_header(info)
        if service_name not in ["moviefav-service"]:
            return lib.gen.http_499_token_required_response(msg="Invalid service name")

        with lib.gen.db.get_engine("psqldb_movie").connect() as db:

            # verify credentials exists
            accountLoginInput.update({"login": accountLoginInput["login"].lower()})
            valid_user_cred = lib.get_user_credentials(db=db, login=accountLoginInput["login"])
            if not valid_user_cred:
                return lib.gen.http_401_unauthorized_response(msg="Invalid credentials")

            # verify that their email has been verified
            if not valid_user_cred["account_info_verified_email"]:
                return lib.gen.http_401_unauthorized_response(msg="Email unverified")

            # verify password
            valid_password = lib.gen.verify_hash_password(password=accountLoginInput["password"].encode('utf8'), hashed=valid_user_cred["account_info_password"].encode('utf8'))
            if not valid_password:
                return lib.gen.http_401_unauthorized_response(msg="Invalid credentials")

            # check active account
            if valid_user_cred["account_info_status"] != "ACTIVE":
                return lib.gen.http_401_unauthorized_response(msg="Account not active")

            # generate token
            token = lib.gen.token_gen(id=valid_user_cred["account_info_id"], service=service_name, reg=valid_user_cred["account_info_registration_status"], status=valid_user_cred["account_info_status"])
            
            response = lib.account_authentication_response(info=info, db=db, token=token, filterInput= {"account_info_id": valid_user_cred["account_info_id"]}, status=valid_user_cred["account_info_registration_status"])
            
            # find pattern match for user then delete
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            search = [
                f"""account_me_query:{valid_user_cred["account_info_id"]}""",
                f"""movie_fav_query:{valid_user_cred["account_info_id"]}:*"""
            ]
            lib.gen.redis_delete_keys_pipe(redis_db, search).execute()      
            
            return response