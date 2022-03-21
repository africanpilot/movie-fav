import os, sys


class AppLibLink:
    @staticmethod
    def make_importables():
        todo = [
            '../../../../links/',
            '../../src/',
        ]
        for rel_path in todo:
            abs_path = os.path.abspath(rel_path)
            if os.path.isdir(abs_path):
                if abs_path not in sys.path:
                    sys.path.append(abs_path)
            else:
                print("app must be run from app_lib directory.")
                exit(1)

AppLibLink.make_importables()