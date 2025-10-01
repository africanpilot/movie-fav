# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from link_lib.microservice_general import LinkGeneral
from link_lib.microservice_generic_model import GenericLinkModel


class GeneralBase(GenericLinkModel, LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@pytest.fixture
def link_general() -> GeneralBase:
    return GeneralBase()
