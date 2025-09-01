# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from link_lib.microservice_general import GeneralJSONEncoder
from movie.src.domain.lib import MovieLib


class GetRemainingMovieCastQuery(MovieLib):
  def __init__(self, **kwargs):
    self.body = kwargs.get('body')

  def execute(self):
    with self.get_connection("psqldb_movie") as db:
      result = self.get_all_movie_cast(db)
  
    return dict(
      message=json.dumps(dict(result), cls=GeneralJSONEncoder),
      received=True
    )
