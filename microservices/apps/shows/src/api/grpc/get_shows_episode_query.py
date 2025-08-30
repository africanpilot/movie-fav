# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_general import GeneralJSONEncoder
from shows.src.domain.lib import ShowsLib


class GetShowsEpisodeQuery(ShowsLib):
  def __init__(self, **kwargs):
    self.body: dict = kwargs.get('body')

  def execute(self):
    self.log.info(f"GetShowsEpisodeQuery: {self.body}")
    with self.get_session("psqldb_shows") as db:
      result = self.get_shows_episode(
        db, self.body.get("shows_info_id"),
        self.body.get("shows_season_id"),
        self.body.get("shows_episode_id")
      )
    
    return dict(
      message=dict(data=json.dumps(dict(result), cls=GeneralJSONEncoder)),
      received=True
    )
