# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


from link_lib.microservice_request import LinkRequest
from shows.src.models.shows_episode import (
    ShowsEpisode,
    ShowsEpisodeCreate,
    ShowsEpisodeRead,
    ShowsEpisodeResponses,
    ShowsEpisodeUpdate,
)
from shows.src.models.shows_info import ShowsInfo, ShowsInfoCreate, ShowsInfoRead, ShowsInfoResponses, ShowsInfoUpdate
from shows.src.models.shows_saga_state import (
    ShowsSagaState,
    ShowsSagaStateCreate,
    ShowsSagaStateRead,
    ShowsSagaStateUpdate,
)
from shows.src.models.shows_season import ShowsSeason, ShowsSeasonCreate, ShowsSeasonRead, ShowsSeasonUpdate


class ShowsModels(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def shows_info(self):
        return ShowsInfo()

    @property
    def shows_info_create(self):
        return ShowsInfoCreate()

    @property
    def shows_info_read(self):
        return ShowsInfoRead()

    @property
    def shows_info_update(self):
        return ShowsInfoUpdate()

    @property
    def shows_info_response(self):
        return ShowsInfoResponses()

    @property
    def shows_saga_state(self):
        return ShowsSagaState()

    @property
    def shows_saga_state_create(self):
        return ShowsSagaStateCreate()

    @property
    def shows_saga_state_read(self):
        return ShowsSagaStateRead()

    @property
    def shows_saga_state_update(self):
        return ShowsSagaStateUpdate()

    @property
    def shows_season(self):
        return ShowsSeason()

    @property
    def shows_season_create(self):
        return ShowsSeasonCreate()

    @property
    def shows_season_read(self):
        return ShowsSeasonRead()

    @property
    def shows_season_update(self):
        return ShowsSeasonUpdate()

    @property
    def shows_episode(self):
        return ShowsEpisode()

    @property
    def shows_episode_create(self):
        return ShowsEpisodeCreate()

    @property
    def shows_episode_read(self):
        return ShowsEpisodeRead()

    @property
    def shows_episode_update(self):
        return ShowsEpisodeUpdate()

    @property
    def shows_episode_response(self):
        return ShowsEpisodeResponses()
