# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from sqlalchemy.sql import text
from colorama import Fore


class AccountMeQuery:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def account_me(self, info):

        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
                    
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            return lib.account_response(info=info, db=db, filterInput={"account_info_id": token_decode["user_id"]}) 