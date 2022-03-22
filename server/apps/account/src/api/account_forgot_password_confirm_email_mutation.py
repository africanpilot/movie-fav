# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from sqlalchemy.sql import text
from colorama import Fore
from datetime import datetime

class AccountForgotPasswordConfirmEmailMutation:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_forgot_password_confirm_email(self, info):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info, email=True)
        if general_validation_payload != "success":
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            data = {
                "account_info_forgot_password_expire_date": str(datetime.fromtimestamp(token_decode["exp"]))
            }
            db.execute(lib.account_modify(id=token_decode["user_id"], data=data))
        
            return lib.gen.success_response(nullPass=True, result={})