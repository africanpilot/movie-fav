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

            return lib.gen.success_response(nullPass=True)