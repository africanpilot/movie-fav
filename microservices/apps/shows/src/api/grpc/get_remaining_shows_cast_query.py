# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_general import GeneralJSONEncoder
from shows.src.domain.lib import ShowsLib


class GetRemainingShowsCastQuery(ShowsLib):
    def __init__(self, **kwargs):
        self.body: dict = kwargs.get("body")

    def execute(self):
        with self.get_session("psqldb_shows") as db:
            result = self.shows_info_read.get_all_shows_cast(db)

        # Convert SQLAlchemy Row to dict properly
        result_dict = result._asdict() if hasattr(result, "_asdict") else dict(result._mapping)

        return dict(message=json.dumps(result_dict, cls=GeneralJSONEncoder), received=True)
