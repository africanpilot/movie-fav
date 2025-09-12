# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property
from typing import Optional
from link_domain.pyratebay import PyratebayLib
from link_lib.microservice_request import LinkRequest

from cinemagoerng import web
from cinemagoerng.model import Movie, TVMovie, TVEpisode


class ImdbNg(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def pyratebay_helper(self):
        return PyratebayLib()

    def get_movie_by_id(self, imdbId: str) -> Movie:
        if not imdbId.startswith("tt"):
            imdbId = "tt" + imdbId
        return web.get_title(imdbId)
    
    def get_movie_info(self, imdbId: str, movie: Movie) -> dict:
        return dict(
            imdb_id=imdbId,
            title=movie.title,
            cast=[item.imdb_id for item in movie.cast] if movie.cast else [],
            year=movie.year,
            directors=[item.name for item in movie.directors] if movie.directors else [],
            genres=movie.genres,
            countries=movie.countries,
            plot=movie.plot.get("en-US") if movie.plot else "",
            cover=movie.primary_image,
            rating=float(movie.rating) if movie.rating else None,
            top_ranking=movie.top_ranking,
            votes=movie.vote_count,
            run_times=[str(movie.runtime)] if movie.runtime else [],
            creators=[item.imdb_id for item in movie.producers] if movie.producers else [],
            full_cover=movie.primary_image,
            release_date=None,
            videos=[],
            download_1080p_url=self.pyratebay_helper.get_magnet_url(movie.title, "1080p"),
            download_720p_url=self.pyratebay_helper.get_magnet_url(movie.title, "720p"),
            download_480p_url=self.pyratebay_helper.get_magnet_url(movie.title, "480p"),
        )

    def get_shows_by_id(self, imdbId: str, season: Optional[str] = None) -> Movie:
        if not imdbId.startswith("tt"):
            imdbId = "tt" + imdbId
        
        if not season:
            return web.get_title(imdbId)
        return web.get_title(imdbId, page="episodes", season=season)

    def get_episode_info(self, show: Movie, episode: TVEpisode): 
        return dict(
            imdb_id=episode.imdb_id,
            shows_imdb_id=show.imdb_id,
            title=episode.title,
            rating=float(episode.rating) if episode.rating else None,
            votes=episode.vote_count,
            release_date=episode.release_date.isoformat() if episode.release_date else None,
            plot=episode.plot.get("en-US") if episode.plot else "",
            year=episode.year,
            episode=episode.episode,
            season=episode.season,
            cover=show.primary_image,
            full_cover=show.primary_image,
            run_times=[str(episode.runtime)] if episode.runtime else [],
            download_1080p_url=self.pyratebay_helper.get_magnet_url(show.title, "1080p", int(episode.season), int(episode.episode)),
            download_720p_url=self.pyratebay_helper.get_magnet_url(show.title, "720p", int(episode.season), int(episode.episode)),
            download_480p_url=self.pyratebay_helper.get_magnet_url(show.title, "480p", int(episode.season), int(episode.episode)),
        )

    def scan_seasons_episodes(self, show: Movie, season: Optional[str] = None, episode: Optional[str] = None) -> int:
        seasons = []
        range_season = [season] if season else range(1, 999)
        for s in range_season:
            try:
                show = self.get_shows_by_id(show.imdb_id, str(s))
                show_season_episodes = list(show.episodes[str(s)].values())[:int(episode)] if episode else list(show.episodes[str(s)].values())
                if show.episodes:
                    seasons.append(dict(
                        season=s,
                        imdb_id=show.imdb_id + "_" + str(s),
                        total_episodes=len(show.episodes[str(s)]),
                        release_date=None,
                        shows_episode=[
                            self.get_episode_info(show, episode)
                            for episode in show_season_episodes
                        ]
                    ))
            except Exception as e:
                break
        return seasons
    
    def get_shows_info(self, imdbId: str, show: Movie, season: Optional[str] = None, episode: Optional[str] = None) -> dict:
        shows_info = dict(
            imdb_id=imdbId,
            title=show.title,
            cast=[item.imdb_id for item in show.cast] if show.cast else [],
            year=show.year,
            directors=[item.name for item in show.directors] if show.directors else [],
            genres=show.genres,
            countries=show.countries,
            plot=show.plot.get("en-US") if show.plot else "",
            cover=show.primary_image,
            total_seasons=None,
            rating=float(show.rating) if show.rating else None,
            votes=show.vote_count,
            run_times=[str(show.runtime)] if show.runtime else [],
            series_years=None,
            creators=[item.imdb_id for item in show.creators] if show.creators else [],
            full_cover=show.primary_image,
            release_date=None,
            videos=[],
            shows_season=[],  # populated later
        )

        seasons = self.scan_seasons_episodes(show, season, episode)
        shows_info["total_seasons"] = len(seasons)
        shows_info["shows_season"] = seasons

        return shows_info
