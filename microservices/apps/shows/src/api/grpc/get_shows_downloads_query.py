# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_general import GeneralJSONEncoder
from shows.src.domain.lib import ShowsLib


class GetShowsDownloadsQuery(ShowsLib):
  def __init__(self, **kwargs):
    self.body: dict = kwargs.get('body')

  def execute(self):
    with self.get_connection("psqldb_shows").connect() as db:
      results = self.get_download_urls(db, self.body.get("imdb_ids"))

    return dict(
      message=json.dumps(dict(result=[dict(r) for r in results]), cls=GeneralJSONEncoder),
      received=True
    )
