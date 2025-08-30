# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
import sys


class AppLibLink:
    @staticmethod
    def make_importables():
        todo = [
            "../../../../links/",
            "../../../../apps/",
            "../../src/",
        ]
        for rel_path in todo:
            abs_path = os.path.abspath(rel_path)
            if os.path.isdir(abs_path):
                if abs_path not in sys.path:
                    sys.path.append(abs_path)
            else:
                print(f"App must be run from app_lib directory or path does not exist: {abs_path}")
                exit(1)


AppLibLink.make_importables()