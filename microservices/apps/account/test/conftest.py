# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest  # noqa: F401
import test_app_lib.link  # noqa: F401

pytest_plugins = [
    "account.test.fixtures.models",
    "link_test.fixtures",
]
