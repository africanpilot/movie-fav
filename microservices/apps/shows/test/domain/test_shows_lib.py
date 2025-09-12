from shows.src.domain.lib import ShowsLib


def test_get_show_info(shows_lib: ShowsLib):
    show_info = shows_lib.process_shows_info("11126994", episode="1")
    assert show_info["imdb_id"] == "11126994"
    assert show_info["title"] == "Arcane: League of Legends"
    assert show_info["year"] == 2021
    assert show_info["total_seasons"] == 2
    assert show_info["rating"] == 9.0
    assert show_info["votes"] >= 411883
    assert "Animation" in show_info["genres"]
    assert "United States" in show_info["countries"]
    assert len(show_info["shows_season"]) == 2
    assert show_info["shows_season"][0]["season"] == 1
    assert show_info["shows_season"][0]["total_episodes"] == 9
    assert isinstance(show_info["cast"], list)
    assert len(show_info["cast"]) > 0
    assert isinstance(show_info["directors"], list)
    assert isinstance(show_info["genres"], list)
    assert isinstance(show_info["countries"], list)
    assert "plot" in show_info
    assert "cover" in show_info
    assert "full_cover" in show_info
    assert "run_times" in show_info
    assert isinstance(show_info["run_times"], list)
    assert "series_years" in show_info
    assert "creators" in show_info
    assert isinstance(show_info["creators"], list)
    assert "release_date" in show_info
    assert "videos" in show_info
    assert isinstance(show_info["videos"], list)
    
    # Assert shows_episode structure and content
    assert "shows_episode" in show_info["shows_season"][0]
    assert isinstance(show_info["shows_season"][0]["shows_episode"], list)
    assert len(show_info["shows_season"][0]["shows_episode"]) > 0
    
    episode = show_info["shows_season"][0]["shows_episode"][0]
    assert episode["imdb_id"] == "tt14586040"
    assert episode["shows_imdb_id"] == "tt11126994"
    assert episode["title"] == "Welcome to the Playground"
    assert episode["rating"] == 8.5
    assert episode["votes"] >= 37760
    assert episode["year"] == 2021
    assert episode["episode"] == "1"
    assert episode["season"] == "1"
    assert episode["release_date"] == "2021-11-06"
    assert "plot" in episode
    assert "cover" in episode
    assert "full_cover" in episode
    assert "run_times" in episode
    assert isinstance(episode["run_times"], list)
    assert episode["download_1080p_url"] is not None
    assert episode["download_720p_url"] is not None
    assert episode["download_480p_url"] is not None
