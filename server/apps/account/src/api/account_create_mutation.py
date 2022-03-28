# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from os import environ

class AccountCreateMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_create(self, info: object, accountCreateInput: dict) -> dict:

        lib = Lib()

        # get service name
        service_name = lib.gen.get_service_from_header(info)
        if service_name not in ["moviefav-service"]:
            return lib.gen.http_401_unauthorized_response(msg="Invaild service name")
        
        # verify email regex
        login_lower = accountCreateInput["login"].lower()
        accountCreateInput.update({"login": login_lower})
        
        # email regex check
        email_reg_check = lib.gen.email_check(accountCreateInput["login"])
        if not email_reg_check:
            return lib.gen.http_401_unauthorized_response(msg="Invalid email format")

        # check password length 
        if len(accountCreateInput["password"]) > 64 or len(accountCreateInput["password"]) < 8:
            return lib.gen.http_401_unauthorized_response(msg="Invalid password legnth")

        # verify password regex
        password_check = lib.gen.password_check(password=accountCreateInput["password"])
        if not password_check:
            return lib.gen.http_401_unauthorized_response(msg="Failed password criteria")

        # check reTypePasswordMatches
        if accountCreateInput["password"] != accountCreateInput["reTypePassword"]:
            return lib.gen.http_401_unauthorized_response(msg="Invalid password retype")

        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            
            # verify login does not exists
            if environ["APP_DEFAULT_ENV"] != "test":
                login_exists = lib.verify_login_exists(db=db, login=accountCreateInput["login"])
                if login_exists == True:
                    return lib.gen.http_401_unauthorized_response(msg="Account already exists")
                
                if login_exists == "DB":
                    lib.gen.log.critical(f"Unable to connect to the database")
                    return lib.gen.http_500_internal_server_error(msg="server connection issues")
             
            # create user sql query
            sql = lib.account_create(data=accountCreateInput)
            
            # send notification
            try:
                response = lib.account_response(info=info, db=db, oneQuery=sql, filterInput={"account_info_email": accountCreateInput["login"]}, extraCols=["account_info_id","account_info_status"])
                # lib.gen.log.info(f"response: {response}")
                # create token
                data = response["result"][0]
                lib.gen.log.info(f"data: {data}")
                token = lib.gen.token_gen(id=data["account_info_id"], service=service_name, hr=24, email=True, status=data["account_info_status"])
                body = {
                    'email': accountCreateInput["login"],
                    'token': token,
                }
                
                msg = lib.gen.send_to_sendgrid(msg=body, template="VerifyEmail")
                lib.gen.log.debug(f"msg: {msg}")
                if not msg:
                    # reverse new account
                    db.execute(lib.delete_user(email=accountCreateInput["login"]))
                    return lib.gen.http_500_internal_server_error(msg="Unable to send email")
                
                return response
            except Exception as e:
                lib.gen.log.debug(f"e: {e}")
                # reverse new account
                db.execute(lib.delete_user(email=accountCreateInput["login"]))
                
                return lib.gen.http_500_internal_server_error(msg="Unknown internal server issue: {e}")           