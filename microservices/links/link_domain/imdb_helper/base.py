# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json
from datetime import datetime
from functools import cached_property
from os import path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from imdb import Cinemagoer
from imdb.Movie import Movie
from link_lib.microservice_request import LinkRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

ia = Cinemagoer()


class ImdbHelper(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def rating_download_url(self) -> str:
        return "https://datasets.imdbws.com/title.ratings.tsv.gz"

    @cached_property
    def rating_download_file_name(self) -> str:
        return "title.ratings.tsv.gz"

    @property
    def moviemeter_base_url(self):
        return "https://m.imdb.com/chart/moviemeter/"

    @property
    def selenium_url(self):
        return "http://selenium:4444/wd/hub"

    @cached_property
    def options(self):
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # to avoid getting detected
        # options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("start-maximized")  # open Browser in maximized mode
        options.add_argument("disable-infobars")  # disabling infobars
        options.add_argument("--disable-extensions")  # disabling extensions
        options.add_argument("--no-sandbox")  # Bypass OS security model
        return options

    @cached_property
    def session_id(self):
        result = self.default_redis_engine.get("chrome_driver_session")
        return json.loads(result).get("session_id") if result else None

    @cached_property
    def driver(self):
        return webdriver.Remote(command_executor=self.selenium_url, options=self.options)

    def get_movie_info_set(self) -> list:
        return ia.get_movie_infoset()

    def get_top_movies(self) -> list:
        return ia.get_top250_movies()

    def get_popular_movies(self) -> list[Movie]:
        return ia.get_popular100_movies()

    @property
    def get_popular_movies_ids(self) -> list[str]:
        return [movie.getID() for movie in self.get_popular_movies()]

    def search_movie_by_title(self, search: str) -> list:
        return ia.search_movie(search)

    def get_movie_by_id(self, imdbId: str) -> Movie:
        return ia.get_movie(imdbId)

    def url_clean(self, url: str) -> str:
        self.log.info(f"Cleaning URL: {url}")
        if url:
            _, ext = path.splitext(url)
            url_filter = url.split("@")[0] + "@" * url.count("@")
            return url_filter.split("._V1_")[0] + ext
        return url

    def get_shows_by_id(self, imdbId: str) -> Movie:
        show = ia.get_movie(imdbId)
        try:
            ia.update(show, "episodes")
        except Exception:
            self.log.critical("Failed to get episodes")
        return show

    def get_popular_shows(self) -> list[Movie]:
        return ia.get_popular100_tv()

    @property
    def get_popular_shows_ids(self) -> list[str]:
        return [shows.getID() for shows in self.get_popular_shows()]

    def get_person_by_id(self, imdbId: str):
        if imdbId.startswith("nm"):
            imdbId = imdbId[2:]
        return ia.get_person(imdbId)

    def get_videos(self, imdbId: str) -> list[str]:
        return ia.get_movie(imdbId).get("videos")

    def download_title_rating(self):
        response = requests.get(self.rating_download_url, allow_redirects=True)
        open(self.rating_download_file_name, "wb").write(response.content)

    def get_top_rating_and_votes(self, limit=100):
        df = pd.read_csv(self.rating_download_file_name, sep="\t")
        df_sort_votes = df.sort_values(by=["numVotes"], ascending=False).head(limit)
        df_sort_rating = df.sort_values(by=["averageRating"], ascending=False).head(limit)
        return list(
            {i.replace("tt", "") for i in list(df_sort_votes["tconst"].tolist() + df_sort_rating["tconst"].tolist())}
        )

    def convert_imdb_date(self, val: str) -> Optional[datetime]:
        if not val:
            return None

        try:
            date = parser.parse(val)
            return date
        except Exception:
            pass

        try:
            date = datetime.strptime(val.split(" (")[0].replace(".", ""), "%d %b %Y")
            return date
        except Exception:
            self.log.info(f"Unable to parse date: {val}")
            return None

    def get_movie_info(self, imdbId: str, data: dict) -> dict:
        return dict(
            imdb_id=imdbId,
            title=data.get("title"),
            cast=[item.getID() for item in data.get("cast")] if data.get("cast") else [],
            year=data.get("year"),
            directors=[item["name"] for item in data.get("directors")] if data.get("directors") else [],
            genres=data.get("genres"),
            countries=data.get("countries"),
            plot=data.get("plot")[0] if data.get("plot") else "",
            cover=self.url_clean(data.get("cover")),
            rating=data.get("rating"),
            votes=data.get("votes"),
            run_times=data.get("runtimes"),
            creators=[item.getID() for item in data.get("creators")] if data.get("creators") else [],
            full_cover=data.get("full-size cover url"),
            release_date=self.convert_imdb_date(data.get("original air date")),
            videos=self.get_videos(imdbId),
        )

    def get_popular_movie_page(self, chart_type: str = "moviemeter") -> BeautifulSoup:
        URL = f"https://m.imdb.com/chart/{chart_type}/"
        page = requests.get(
            URL,
            headers=dict(
                accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                accept_language="en-US,en;q=0.9",
                cache_control="max-age=0",
                cookie="session-id=136-3316153-1135861; session-id-time=2082787201l; ubid-main=135-2048450-7603625; ad-oo=0; _cc_id=b934828766b6987dad45ad0773664f08; panoramaId_expiry=1735322686768; ci=e30; _au_1d=AU1D-0100-001735236288-J95BIEY0-EE2T; _ga=GA1.1.1720485033.1735236309; 33acrossIdTp=Y%2FXyibEVYClAhtTOX%2FJvzQk2TP143YdvlawgYfpvmgo%3D; _ga_FVWZ0RM4DH=GS1.1.1735236308.1.1.1735236798.47.0.0; __gads=ID=3c6dfd3b69a5b10a:T=1735237795:RT=1735237795:S=ALNI_MbsiYHOYAlOt6z6KVV4rACL3iEgmw; __gpi=UID=00000faba1aeadc2:T=1735237795:RT=1735237795:S=ALNI_MYO8cBjGge-9OAnAcyc3dBQvycspg; __eoi=ID=496be07487c4320f:T=1735237795:RT=1735237795:S=AA-AfjZgELyWlC7lvA2B_1IOlwVV; session-token=1vcOCh3dio5WIiT+o0Duyn5+tr8VJeBixlVoZmDsdbSGbBlcx7aOmLurPHSi0OFrplKhkLn9hEIDp9DujFGxCDnx1lTN9VCD3xySWXg5C0jijTGTDq2OrIija+ow3SBzF3r8/ZS8NYomoaNosjMbRYzoThVda4xkj9h94BRXCzauhb458NyUuqdDHrcQWUYiuY53RIttfTAgoe1QiXSkIQRJzFeqQvABPVqOBrSCmZ6AJy6rzzTZusyZYaofb4C/aMrVy/gBcfyHxxJu8cSikC1vqAZsxtVjt3pY+xq6WPW2sZ4bzX91MRa7MnZ1KwEjYQtvXW4ch07NruviOhKdpdtDkH/bOVuU; csm-hit=tb:s-JTDEP2KXFCDAY077KHBC|1735239509390&t:1735239509656&adb:adblk_no",
                priority="u=0, i",
                sec_fetch_dest="document",
                sec_fetch_mode="navigate",
                sec_fetch_site="none",
                sec_fetch_user="?1",
                upgrade_insecure_requests="1",
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            ),
        )

        # check if status code
        if page.status_code != 200:
            self.log.info(f"Unable to get page from {URL} at error {page.reason}")
            return {}

        soup = BeautifulSoup(page.content, "html.parser")

        result = soup.find(
            "div", class_="ipc-page-content-container ipc-page-content-container--center sc-f91e97af-0 jbRgdG"
        )

        return result

    def get_imdb_popular(self, soup: BeautifulSoup):
        total = []
        for a in soup.find_all("li"):
            try:
                total.append(a.find("a")["href"].split("/")[2].replace("tt", ""))
            except BaseException:
                continue
        return total

    def get_shows_episode_page(self, imdb_id: str, season: int) -> BeautifulSoup:
        URL = f"https://m.imdb.com/title/tt{imdb_id}/episodes/?season={season}"
        page = requests.get(
            URL,
            headers=dict(
                authority="m.imdb.com",
                accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                accept_language="en-US,en;q=0.9",
                cache_control="max-age=0",
                cookie="session-id=132-9381883-3296534; session-id-time=2082787201l; ubid-main=131-0923015-7728101; ci=e30; ad-oo=0; session-token=U7R6Gic8y1yrn2UheyVG2bfWGEbhVsLVDNaRvdKIKd6StGYol2gu1lLaF72QBxmDXS4Rdt6eS3qsZ0g+JaVI9dVRlkl0hHaUMX/KOPbiIWDt8KIcfcjfPeyQPCgsSDIy9082ew7D9j9wNQpQOIm7EMkQXWRFoFR1VfLJjC9F6xQAxqC1e8Sfdr+oN9raevS4Cvb44F9TzWt5u4EltNLTmgfnvEdyEg1PuQZYOh+m0S+U3ChO8ZBFaYuM7xaXgx0M0lcTvX8Z5A+g88no41buKwHHx7NWN42jfmE3r6gMjmTFAzqop9YDqRIiW4Cb69AbXHzhSx/udWyPu65jwD/1VMRsISeBlZyt; csm-hit=tb:s-SHA7XHAVP41YCG2CZJ3X|1709521796555&t:1709521796752&adb:adblk_yes",
                sec_ch_ua='"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                sec_ch_ua_mobile="?1",
                sec_ch_ua_platform='"Android"',
                sec_fetch_dest="document",
                sec_fetch_mode="navigate",
                sec_fetch_site="none",
                sec_fetch_user="?1",
                upgrade_insecure_requests="1",
                user_agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            ),
        )

        # check if status code
        if page.status_code != 200:
            self.log.info(f"Unable to get page from {URL}")
            return {}

        soup = BeautifulSoup(page.content, "html.parser")

        result = soup.find("section", class_="ipc-page-section ipc-page-section--base ipc-page-section--sp-pageMargin")

        return result

    def get_shows_episodes(self, soup: BeautifulSoup):
        total = []
        for a in soup.find_all("article"):
            try:
                total.append(a.find("a")["href"].split("/")[2].replace("tt", ""))
            except BaseException:
                continue
        return total

    def access_site(self) -> None:
        self.log.info(f"accessing site: {self.moviemeter_base_url}")
        self.driver.get(self.moviemeter_base_url)
        self.driver.implicitly_wait(10)

    def create_driver_session(self):
        # access sites
        if not self.session_id:
            self.access_site()

    def get_charts_imdbs(self, cat: str = "moviemeter") -> list[str]:
        redis_result = self.movie_redis_engine.get(f"get_charts_imdbs:{cat}")
        if redis_result:
            response = json.loads(redis_result)
            return response.get("result")

        if not self.session_id:
            self.log.info(f"accessing site: https://m.imdb.com/chart/{cat}/")
            self.driver.get(f"https://m.imdb.com/chart/{cat}/")
            self.driver.implicitly_wait(10)

        content = self.driver.find_elements(by=By.TAG_NAME, value="a")
        data = [element.get_attribute("href") for element in content]
        data_f: list[str] = list(filter(lambda item: "https://m.imdb.com/title/" in item, data))

        result = [i.split("/")[4].replace("tt", "") for i in data_f]

        self.load_to_redis(self.movie_redis_engine, f"get_charts_imdbs:{cat}", dict(result=result), ex=86400)

        return result

    def get_person_info(self, imdbId: str, data: dict) -> dict:
        return dict(
            imdb_id=imdbId,
            name=data.get("name"),
            birth_place=data.get("birth info").get("birth place") if data.get("birth info") else None,
            akas=data.get("akas"),
            filmography=(
                [item.getID() for item in data.get("filmography").get("actress", [])]
                + [item.getID() for item in data.get("filmography").get("actor", [])]
                if data.get("filmography")
                else None
            ),
            mini_biography=data.get("mini biography")[0] if data.get("mini biography") else None,
            birth_date=self.convert_imdb_date(data.get("birth date")),
            titles_refs=[v.getID() for k, v in data.get("titlesRefs").items()] if data.get("titlesRefs") else None,
            head_shot=self.url_clean(data.get("headshot")),
        )

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
        )

    def get_shows_info(self, imdbId: str, data: dict) -> dict:
        self.log.info(
            f"Parsing shows info for {imdbId} data={data.get('cover')} number of seasons={data.get('number of seasons')} {dir(data)}"
        )
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
                total_seasons=data.get("number of seasons"),
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
                        total_episodes=(
                            len(data["episodes"][s]) if data.get("episodes") and data.get("episodes").get(s) else None
                        ),
                        release_date=(
                            self.convert_imdb_date(data["episodes"][s][1].get("original air date"))
                            if data.get("episodes") and data.get("episodes").get(s)
                            else None
                        ),
                    ),
                    episodes=[
                        self.parse_episode_info(epi_imdb, imdbId, data)
                        for epi_imdb in self.get_shows_episodes(self.get_shows_episode_page(imdbId, s))
                    ],
                )
                for s in range(1, data.get("number of seasons") + 1)
            ],
        )
