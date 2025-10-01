# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from shows.src.domain.lib import ShowsLib


class GetAllShowsSeasonQuery(ShowsLib):
    def __init__(self, **kwargs):
        self.body: dict = kwargs.get("body")

    def execute(self):
        self.log.info(f"GetAllShowsSeasonQuery: {self.body}")
        with self.get_session("psqldb_shows") as db:
            result = self.shows_season_read.get_all_shows_seasons(db, self.body.get("shows_info_id"))

        seasons = list({r.id for r in result})
        return dict(message=dict(data=seasons), received=True)
