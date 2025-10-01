# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from shows.src.domain.lib import ShowsLib


class GetShowsQuery(ShowsLib):
    def __init__(self, **kwargs):
        self.body = kwargs.get("body")

    def execute(self):
        self.log.info(f"GetShowsQuery: {self.body}")
        with self.get_session("psqldb_shows") as db:
            result = self.shows_info_read.get_show_by_id(db, self.body.get("shows_info_id"))

        shows = list({r.id for r in result})
        return dict(message=dict(data=shows), received=True)
