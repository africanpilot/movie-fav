import pytest
from link_lib.microservice_general import LinkGeneral
from person.src.domain.lib import PersonLib

# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.person_domain, pytest.mark.person])


@GENERAL_PYTEST_MARK
@pytest.mark.person_bench
def test_get_person_info(benchmark, person_lib: PersonLib):
    person_info = person_lib.process_person_info("0000206")
    assert person_info["imdb_id"] == "0000206"
    assert person_info["name"] == "Keanu Reeves"
    assert person_info["birth_place"] is None
    assert person_info["akas"] is None
    assert person_info["filmography"] is None
    assert person_info["mini_biography"] is None
    assert person_info["birth_date"] is None
    assert person_info["titles_refs"] is None
    assert (
        person_info["head_shot"]
        == "https://m.media-amazon.com/images/M/MV5BNDEzOTdhNDUtY2EyMy00YTNmLWE5MjItZmRjMmQzYTRlMGRkXkEyXkFqcGc@.jpg"
    )

    benchmark(person_lib.process_person_info, "0000206")
