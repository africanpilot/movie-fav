# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property
from link_domain.pyratebay import PyratebayLib
from link_lib.microservice_request import LinkRequest

from cinemagoerng import web
from cinemagoerng.model import Movie


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
