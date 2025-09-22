# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_general import LinkGeneral
from shows.src.models.shows_episode.base import ShowsEpisode
from sqlalchemy import delete
from sqlalchemy.engine.base import Connection


class ShowsEpisodeDelete(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def shows_episode_delete(self, db: Connection, shows_id: int, commit: bool = True) -> None:
        sql_query = delete(ShowsEpisode).where(ShowsEpisode.id == shows_id)

        if commit:
            db.execute(sql_query)
        return sql_query
