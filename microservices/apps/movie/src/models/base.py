# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property

from link_lib.microservice_request import LinkRequest
from movie.src.models.movie_info import MovieInfo, MovieInfoCreate, MovieInfoRead, MovieInfoResponses, MovieInfoUpdate
from movie.src.models.movie_saga_state import (
    MovieSagaState,
    MovieSagaStateCreate,
    MovieSagaStateRead,
    MovieSagaStateUpdate,
)


class MovieModels(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def movie_info(self):
        return MovieInfo()

    @cached_property
    def movie_info_create(self):
        return MovieInfoCreate()

    @cached_property
    def movie_info_read(self):
        return MovieInfoRead()

    @cached_property
    def movie_info_update(self):
        return MovieInfoUpdate()

    @cached_property
    def movie_info_response(self):
        return MovieInfoResponses()

    @cached_property
    def movie_saga_state(self):
        return MovieSagaState()

    @cached_property
    def movie_saga_state_create(self):
        return MovieSagaStateCreate()

    @cached_property
    def movie_saga_state_read(self):
        return MovieSagaStateRead()

    @cached_property
    def movie_saga_state_update(self):
        return MovieSagaStateUpdate()
