# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from typing import Optional
from datetime import datetime
from sqlalchemy.engine.base import Connection
from link_domain.imdb import ImdbHelper
from link_lib.microservice_request import LinkRequest
from shows.src.models.shows_info import ShowsInfoRead, ShowsInfoUpdate, ShowsInfoCreate, ShowsInfoResponses, ShowsInfoResponse
from shows.src.models.shows_season import ShowsSeasonRead
from shows.src.models.shows_episode import ShowsEpisodeRead, ShowsEpisodeUpdate, ShowsEpisodeResponse
from dateutil import parser
from shows.src.models.shows_saga_state import (
    ShowsSagaStateCreate, ShowsSagaStateRead, ShowsSagaStateUpdate
)

from link_domain.pyratebay import PyratebayLib


class ShowsLib(
    ShowsInfoRead, ShowsInfoCreate, ShowsInfoUpdate, ShowsInfoResponses,
    ShowsSeasonRead, ShowsEpisodeRead, ShowsEpisodeUpdate,
    ShowsSagaStateCreate, ShowsSagaStateRead, ShowsSagaStateUpdate,
    PyratebayLib, ImdbHelper, LinkRequest
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def convert_imdb_date(self, val: str) -> Optional[datetime]:
        if not val:
            return None

        try:
            date = parser.parse(val)
            return date
        except Exception:
            pass
        
        try:
            date = datetime.strptime(val.split(" (")[0].replace(".",""), '%d %b %Y')
            return date
        except Exception:
            self.log.info(f"Unable to parse date: {val}")
        
        return None
    
    def get_episode_info(self, episode, shows_imdb_id: str, data: dict):
        episode_info = self.get_movie_by_id(episode.getID())
        
        return dict(
            imdb_id=episode.getID(),
            shows_imdb_id=shows_imdb_id,
            title=episode.get("title"),
            rating=episode.get("rating"),
            votes=episode.get("votes"),
            release_date=self.convert_imdb_date(episode.get("original air date")),
            plot=episode.get("plot"),
            year=episode.get("year"),
            episode=episode.get("episode"),
            season=episode.get("season"),
            cover=self.url_clean(episode_info.get("cover")),
            full_cover=episode_info.get("full-size cover url"),
            run_times=episode_info.get("runtimes"),
            download_1080p_url=self.get_magnet_url(data.get("title"), "1080p", int(episode.get("season")), int(episode.get("episode"))),
            download_720p_url=self.get_magnet_url(data.get("title"), "720p", int(episode.get("season")), int(episode.get("episode"))),
            download_480p_url=self.get_magnet_url(data.get("title"), "480p", int(episode.get("season")), int(episode.get("episode"))),
        )
        
    def parse_episode_info(self, shows_episode_imdb: str, shows_imdb_id: str, data: dict):
        episode_info = self.get_movie_by_id(shows_episode_imdb)
        
        return dict(
            imdb_id=shows_episode_imdb,
            shows_imdb_id=shows_imdb_id,
            title=episode_info.get("title"),
            rating=episode_info.get("rating"),
            votes=episode_info.get("votes"),
            release_date=self.convert_imdb_date(episode_info.get("original air date")),
            plot=episode_info.get("plot"),
            year=episode_info.get("year"),
            episode=episode_info.get("episode"),
            season=episode_info.get("season"),
            cover=self.url_clean(episode_info.get("cover")),
            full_cover=episode_info.get("full-size cover url"),
            run_times=episode_info.get("runtimes"),
            download_1080p_url=self.get_magnet_url(data.get("title"), "1080p", int(episode_info.get("season")), int(episode_info.get("episode"))),
            download_720p_url=self.get_magnet_url(data.get("title"), "720p", int(episode_info.get("season")), int(episode_info.get("episode"))),
            download_480p_url=self.get_magnet_url(data.get("title"), "480p", int(episode_info.get("season")), int(episode_info.get("episode"))),
        )

    def get_shows_info(self, imdbId: str, data: dict) -> dict:
        return dict(
            shows_info=dict(
                imdb_id=imdbId,
                title=data.get("title"),
                cast=[item.getID() for item in data.get("cast")] if data.get("cast") else [],
                year=data.get("year"),
                directors=[item["name"] for item in data.get("directors")] if data.get("directors") else [],
                genres=data.get("genres"),
                countries=data.get("countries"),
                plot=data.get("plot")[0] if data.get("plot") else "",
                cover=self.url_clean(data.get("cover")),
                total_seasons=data.get('number of seasons'),
                rating=data.get("rating"),
                votes=data.get("votes"),
                run_times=data.get("runtimes"),
                series_years=data.get("series years"),
                creators=[item.getID() for item in data.get("creators")] if data.get("creators") else [],
                full_cover=data.get("full-size cover url"),
                release_date=self.convert_imdb_date(data.get("original air date")),
                videos=self.get_videos(imdbId),
            ),
            shows_season=[
                dict(
                    season=dict(
                        season=s,
                        imdb_id=imdbId + "_" + str(s),
                        total_episodes=len(data['episodes'][s]) if data.get('episodes') and data.get('episodes').get(s) else None,
                        release_date=self.convert_imdb_date(data['episodes'][s][1].get('original air date')) if data.get('episodes') and data.get('episodes').get(s) else None,
                    ),
                    episodes=[
                        self.parse_episode_info(epi_imdb, imdbId, data)
                        for epi_imdb in self.get_shows_episodes(self.get_shows_episode_page(imdbId, s))
                    ]
                )
                for s in range(1, data.get('number of seasons') + 1)
            ]
        )

    def shows_info_query_redis_load(self, key) -> ShowsInfoResponse:
        redis_result = self.shows_redis_engine.get(f"""shows_info_query:{key}""")
        if not redis_result:
            return None

        return self.load_from_redis(ShowsInfoResponse, redis_result)

    def shows_info_query_redis_dump(self, key, response: ShowsInfoResponse):
        redis_conv = response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        self.load_to_redis(self.shows_redis_engine, f"shows_info_query:{key}", redis_conv)

    def redis_delete_shows_info_keys(self) -> None:
        self.redis_delete_keys_pipe(self.shows_redis_engine, [f"shows_info_query:*"]).execute()

    def shows_episode_query_redis_load(self, key) -> ShowsEpisodeResponse:
        redis_result = self.shows_redis_engine.get(f"""shows_episode_query:{key}""")
        if not redis_result:
            return None

        return self.load_from_redis(ShowsEpisodeResponse, redis_result)
    
    def shows_episode_query_redis_dump(self, key, response: ShowsEpisodeResponse) -> None:
        redis_conv = response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        self.load_to_redis(self.shows_redis_engine, f"shows_episode_query:{key}", redis_conv)
        
    def redis_delete_shows_episode_keys(self) -> None:
        self.redis_delete_keys_pipe(self.shows_redis_engine, [f"shows_episode_query:*"]).execute()

    def shows_saga_redis_update(self, keys: list[bytes]) -> tuple[list, list]:
        return keys, [
            self.shows_state_saga_update(self.get_key(key, 2), **json.loads(state))
            for key,state in zip(keys, self.shows_redis_engine.mget(keys)) if state
        ]

    def shows_info_redis_create(self, key_match: str = None, keys: list[str] = None, db: Connection = None) -> tuple[list, list]:
        keys = self.search_key(self.shows_redis_engine, key_match, 1000) if not keys else keys
        if not keys:
            return [],[]

        remaining_keys = [k for k in keys if k is not None]
        
        if not remaining_keys:
            return [],[]

        queries = []
        for key,state in zip(remaining_keys, self.shows_redis_engine.mget(remaining_keys)):
            queries = queries + self.shows_info_create_imdb(db, json.loads(state))
        
        return remaining_keys, queries
