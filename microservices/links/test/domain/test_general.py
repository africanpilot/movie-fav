# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest

from link_test.fixtures.link_domain import GeneralBase
from link_lib.microservice_general import LinkGeneral


# add general pytest markers
GENERAL_PYTEST_MARK = LinkGeneral().compose_decos([pytest.mark.trackstar_domain_general, pytest.mark.trackstar])

@GENERAL_PYTEST_MARK
def test_always_passes():
  assert True

@GENERAL_PYTEST_MARK
def test_fil_json_keys(benchmark, link_general: GeneralBase):
	# test works
  dict_data = dict(name="bob", age=30, home="here")
  result = link_general.fil_json_keys(x=dict_data, y=["home"])

  assert result == dict(home="here")

  # run benchmark
  benchmark(link_general.fil_json_keys, x=dict_data, y=["home"])

@GENERAL_PYTEST_MARK
def test_remove_keys(benchmark, link_general: GeneralBase):
	# test works
  dict_data = [dict(name="bob", age=30, home="here")]
  result = link_general.remove_keys(data=dict_data, exclude=["home"])

  assert result == [dict(name="bob", age=30)]

  # run benchmark
  benchmark(link_general.remove_keys, data=dict_data, exclude=["home"])

@GENERAL_PYTEST_MARK
def test_rand_word_gen_range(benchmark, link_general: GeneralBase):
	# test works
  result = link_general.rand_word_gen_range(start=5, end=15)

  assert len(result) >= 5
  assert len(result) <= 15

  # run benchmark
  benchmark(link_general.rand_word_gen_range, start=5, end=15)

@GENERAL_PYTEST_MARK
def test_rand_word_gen_range(benchmark, link_general: GeneralBase):
	# test works
  result = link_general.rand_word_gen_range(start=5, end=15)

  assert len(result) >= 5
  assert len(result) <= 15

  # run benchmark
  benchmark(link_general.rand_word_gen_range, start=5, end=15)

@GENERAL_PYTEST_MARK
def test_compose_decos(benchmark, link_general: GeneralBase):
	# test works
  markers = link_general.compose_decos([pytest.mark.link_domain_general, pytest.mark.skeleton])

  assert markers is not None

  # run benchmark
  benchmark(link_general.compose_decos, [pytest.mark.link_domain_general, pytest.mark.skeleton])
