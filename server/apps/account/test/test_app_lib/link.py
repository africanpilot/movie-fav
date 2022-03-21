# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os, sys
class TestAppLibLink:
    @staticmethod
    def make_importables():
        
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

        todo = [
            '../../../../links/',
            '../../src/',
            '../../test/',
        ]
        for rel_path in todo:
            abs_path = os.path.abspath(rel_path)
            if os.path.isdir(abs_path):
                if abs_path not in sys.path:
                    sys.path.append(abs_path)
            else:
                print(f"Could not find {abs_path}")
                print("Weird. Please contact microservices admin for help.")
                exit(1)

TestAppLibLink.make_importables()