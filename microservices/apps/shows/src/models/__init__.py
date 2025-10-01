from shows.src.models.base import ShowsModels
from shows.src.models.shows_episode import ShowsEpisode
from shows.src.models.shows_info import ShowsInfo
from shows.src.models.shows_saga_state import ShowsSagaState
from shows.src.models.shows_season import ShowsSeason

__all__ = (
    "ShowsInfo",
    "ShowsSeason",
    "ShowsEpisode",
    "ShowsSagaState",
    "ShowsModels",
)

ALL_MODELS = [
    ShowsInfo,
    ShowsSeason,
    ShowsEpisode,
    ShowsSagaState,
]
