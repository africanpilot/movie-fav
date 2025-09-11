# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property
from shows.src.models.shows_info import ShowsInfo, ShowsInfoCreate, ShowsInfoRead, ShowsInfoUpdate, ShowsInfoResponses
from shows.src.models.shows_saga_state import ShowsSagaState, ShowsSagaStateCreate, ShowsSagaStateRead, ShowsSagaStateUpdate
from shows.src.models.shows_season import ShowsSeason, ShowsSeasonCreate, ShowsSeasonRead, ShowsSeasonUpdate
from shows.src.models.shows_episode import ShowsEpisode, ShowsEpisodeCreate, ShowsEpisodeRead, ShowsEpisodeUpdate, ShowsEpisodeResponses
from link_lib.microservice_request import LinkRequest


class ShowsModels(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def shows_info(self):
        return ShowsInfo()
    
    @cached_property
    def shows_info_create(self):
        return ShowsInfoCreate()
    
    @cached_property
    def shows_info_read(self):
        return ShowsInfoRead()
    
    @cached_property
    def shows_info_update(self):
        return ShowsInfoUpdate()
    
    @cached_property
    def shows_info_response(self):
        return ShowsInfoResponses()
    
    @cached_property
    def shows_saga_state(self):
        return ShowsSagaState()
    
    @cached_property
    def shows_saga_state_create(self):
        return ShowsSagaStateCreate()
    
    @cached_property
    def shows_saga_state_read(self):
        return ShowsSagaStateRead()
    
    @cached_property
    def shows_saga_state_update(self):
        return ShowsSagaStateUpdate()
    
    @cached_property
    def shows_season(self):
        return ShowsSeason()

    @cached_property
    def shows_season_create(self):
        return ShowsSeasonCreate()

    @cached_property
    def shows_season_read(self):
        return ShowsSeasonRead()

    @cached_property
    def shows_season_update(self):
        return ShowsSeasonUpdate()

    @cached_property
    def shows_episode(self):
        return ShowsEpisode()

    @cached_property
    def shows_episode_create(self):
        return ShowsEpisodeCreate()

    @cached_property
    def shows_episode_read(self):
        return ShowsEpisodeRead()

    @cached_property
    def shows_episode_update(self):
        return ShowsEpisodeUpdate()

    @cached_property
    def shows_episode_response(self):
        return ShowsEpisodeResponses()
