# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from link_lib.microservice_general import GeneralJSONEncoder
from shows.src.domain.lib import ShowsLib


class GetRemainingShowsCastQuery(ShowsLib):
  def __init__(self, **kwargs):
    self.body: dict = kwargs.get('body')

  def execute(self):
    with self.get_session("psqldb_shows") as db:
      result = self.get_all_shows_cast(db)
  
    return dict(
      message=json.dumps(dict(result), cls=GeneralJSONEncoder),
      received=True
    )
