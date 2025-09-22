# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from account.src.controller.controller_api import APIController
from account.src.domain.lib import AccountLib
from link_models.enums import SchemaTypeEnum


@pytest.fixture
def link_account_lib() -> AccountLib:
    return AccountLib()


@pytest.fixture
def private_schema():
    return APIController(schema_type=SchemaTypeEnum.PRIVATE).get_graphql_schema()
