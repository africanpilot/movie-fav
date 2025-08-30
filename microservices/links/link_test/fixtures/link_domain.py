# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from link_domain.imdb.base import ImdbHelper

from link_lib.microservice_generic_model import GenericLinkModel
from link_lib.microservice_general import LinkGeneral
from link_lib.microservice_request import LinkRequest
from link_lib.microservice_response import LinkResponse


class GeneralBase(GenericLinkModel, LinkGeneral):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
class GeneralRequest(GenericLinkModel, LinkRequest):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    
class GeneralLinkResponse(GenericLinkModel, LinkResponse):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)


class GeneralImdbHelper(GenericLinkModel, ImdbHelper):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)


@pytest.fixture
def link_general() -> GeneralBase:
  return GeneralBase()


@pytest.fixture
def link_request() -> GeneralRequest:
  return GeneralRequest()


@pytest.fixture
def link_response() -> GeneralLinkResponse:
  return GeneralLinkResponse()

@pytest.fixture
def link_imdb_helper() -> GeneralImdbHelper:
  return GeneralImdbHelper()
