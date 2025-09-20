import pytest
from link_lib.microservice_general import LinkGeneral
from movie.src.domain.lib import MovieLib


# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.movie_domain, pytest.mark.movie])

@GENERAL_PYTEST_MARK
@pytest.mark.movie_bench
def test_get_movie_info(benchmark, movie_lib: MovieLib):
    movie_info = movie_lib.process_movie_info("tt0133093")  # The Matrix
    assert movie_info["title"] == "The Matrix"
    assert movie_info["year"] == 1999
    assert movie_info["imdb_id"] == "0133093"
    assert movie_info["directors"] == ["Lana Wachowski", "Lilly Wachowski"]
    assert "nm0000206" in movie_info["cast"]
    assert movie_info["genres"] == ["Action", "Sci-Fi"]
    assert movie_info["countries"] == ["United States", "Australia"]
    assert movie_info["plot"].startswith("When a beautiful stranger leads computer hacker Neo")
    assert movie_info["cover"].startswith("https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_.jpg")
    assert movie_info["rating"] >= 8.7
    assert movie_info["votes"] >= 2000000
    assert movie_info["run_times"] == ["136"]
    assert "nm0075732" in movie_info["creators"]
    assert movie_info["full_cover"].startswith("https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_.jpg")
    assert movie_info["release_date"] == None
    assert movie_info["videos"] == []

    benchmark(movie_lib.process_movie_info, "0133093")
