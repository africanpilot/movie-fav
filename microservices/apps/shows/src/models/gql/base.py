# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from pydantic import BaseModel


class ShowsDownloadInput(BaseModel):
    imdb_id: str
    shows_imdb_id: str
    season: int
    episode: int
