# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_general import GeneralJSONEncoder
from movie.src.domain.lib import MovieLib


class GetMovieDownloadsQuery(MovieLib):
  def __init__(self, **kwargs):
    self.body: dict = kwargs.get('body')

  def execute(self):
    with self.get_connection("psqldb_movie").connect() as db:
      results = self.get_download_urls(db, self.body.get("imdb_ids"))

    return dict(
      message=json.dumps(dict(result=[dict(r) for r in results]), cls=GeneralJSONEncoder),
      received=True
    )
