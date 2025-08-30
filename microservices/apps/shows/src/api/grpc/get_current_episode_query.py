# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_general import GeneralJSONEncoder
from shows.src.domain.lib import ShowsLib


class GetCurrentEpisodeQuery(ShowsLib):
  def __init__(self, **kwargs):
    self.body: dict = kwargs.get('body')

  def execute(self):
    self.log.info(f"GetCurrentEpisodeQuery: {self.body}")
    with self.get_session("psqldb_shows") as db:
      result = self.get_current_episode(db, self.body.get("shows_info_id"))
    
    return dict(
      message=json.dumps(dict(result), cls=GeneralJSONEncoder),
      received=True
    )
