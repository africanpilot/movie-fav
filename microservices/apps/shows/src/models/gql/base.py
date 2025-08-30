# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from pydantic import BaseModel
from link_models.enums import DownloadTypeEnum


class ShowsDownloadInput(BaseModel):
    imdb_id: str
    shows_imdb_id: str
    season: int
    episode: int
    download_type: DownloadTypeEnum = DownloadTypeEnum.DOWNLOAD_1080p
