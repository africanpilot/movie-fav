# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib

class AccountForgotPasswordMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_forgot_password(self, info: object, accountLogin: str) -> dict:
        
        lib = Lib()
        
        # get service name
        service_name = lib.gen.get_service_from_header(info)
        if service_name not in ["moviefav-service"]:
            return lib.gen.http_499_token_required_response(msg="Invalid service name")

        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        
            # verify credentials exists
            valid_user_cred = lib.get_user_credentials(db=db, login=accountLogin)
            if not valid_user_cred:
                return lib.gen.http_401_unauthorized_response(msg="Account does not exist")

            # create token
            token = lib.gen.token_gen(id=valid_user_cred["account_info_id"], service=service_name, hr=24, email=True, status=valid_user_cred["account_info_status"])

            # send notification
            body = {
                'email': accountLogin,
                'token': token,
                'user_id': valid_user_cred["account_info_id"],
            }
            msg = lib.gen.send_to_sendgrid(msg=body, template="ForgotPassword")
            if not msg:
                return lib.gen.http_500_internal_server_error(msg="Unable to send email")

            # find pattern match for user then delete
            redis_db = lib.gen.db.get_engine("redisdb_movie", "redis")
            lib.gen.redis_delete_keys_pipe(redis_db, f"""account_me_query:{valid_user_cred["account_info_id"]}""").execute()      
             
            return lib.gen.success_response(nullPass=True, result={})

            




            



