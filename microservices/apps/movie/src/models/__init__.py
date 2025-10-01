from movie.src.models.base import MovieModels
from movie.src.models.movie_info import MovieInfo
from movie.src.models.movie_saga_state import MovieSagaState

__all__ = (
    "MovieModels",
    "MovieInfo",
    "MovieSagaState",
)

ALL_MODELS = [
    MovieInfo,
    MovieSagaState,
]
