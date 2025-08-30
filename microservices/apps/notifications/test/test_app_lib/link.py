# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
import sys


class TestAppLibLink:
    @staticmethod
    def make_importables():

        os.chdir(os.path.abspath(os.path.dirname(__file__)))

        todo = [
            "../../../../links/",
            "../../../../apps/",
            "../../src/",
            "../../test/",
        ]
        for rel_path in todo:
            abs_path = os.path.abspath(rel_path)
            if os.path.isdir(abs_path):
                if abs_path not in sys.path:
                    sys.path.append(abs_path)
            else:
                print(f"App must be run from test_app_lib directory or path does not exist: {abs_path}")
                exit(1)


TestAppLibLink.make_importables()