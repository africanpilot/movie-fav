# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_general import GeneralJSONEncoder
from movie.src.domain.lib import MovieLib


class GetRemainingMovieCastQuery(MovieLib):
    def __init__(self, **kwargs):
        self.body = kwargs.get("body")

    def execute(self):
        with self.get_session("psqldb_movie") as db:
            result = self.movie_info_read.get_all_movie_cast(db)

        # Convert SQLAlchemy Row to dict properly
        result_dict = result._asdict() if hasattr(result, "_asdict") else dict(result._mapping)

        return dict(message=json.dumps(result_dict, cls=GeneralJSONEncoder), received=True)
