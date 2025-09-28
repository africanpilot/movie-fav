# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from account.src.domain.lib import AccountLib


@pytest.fixture
def account_lib() -> AccountLib:
    return AccountLib()
