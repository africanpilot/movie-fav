# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
import sys
import logging

class MicroserviceDynamicLinkImport:
    """
    Allow a link/foo_bar class to be instantiated simply by creating a class named "fooBar".
    Simplify wiring up modules in the higher level microservice code. See MicroserviceLinkDynamic()
    """

    @staticmethod
    def __camel_to_snake(camel: str) -> str:
        snake = ""
        str_len = len(camel)

        if str_len > 1:
            for i in range(0, str_len - 1):
                snake += camel[i].lower()
                if camel[i].islower() and camel[i + 1].isupper():
                    snake += "_"
            snake += camel[str_len - 1].lower()
        else:
            snake = camel.lower()

        return snake

    @staticmethod
    def load_module(relative_paths, camel):
        snake = MicroserviceDynamicLinkImport.__camel_to_snake(camel)
        try:
            absolute_directory = next(
                os.path.abspath(p) for p in relative_paths if os.path.isfile(os.path.abspath(p) + "/" + snake + ".py")
            )
            # logging.info("Adding from: " + str([os.path.abspath(p) for p in relative_paths]) + " | " + snake + ".py")
        except StopIteration:
            file = str([os.path.abspath(p) for p in relative_paths]) + " | " + snake + ".py"
            logging.critical("Could not find expected file: " + file)
            exit(1)

        if absolute_directory not in sys.path:
            sys.path.append(absolute_directory)

        m = __import__(snake)
        return m

    @staticmethod
    def get_class(relative_paths, camel):
        m = MicroserviceDynamicLinkImport.load_module(relative_paths, camel)
        cls = getattr(m, camel)
        return cls

    @staticmethod
    def fork(relative_paths, camel, **kwargs):
        cls = MicroserviceDynamicLinkImport.get_class(relative_paths, camel)
        obj = cls(**kwargs)
        return obj

    @staticmethod
    def by_string(name, **kwargs):
        path = "../../../../links/link_lib"
        obj = MicroserviceDynamicLinkImport.fork(path, name, **kwargs)
        return obj


class MicroserviceDynamicLink:
    """
    If you define a class named FooBar using this base class:
    On instantiation it becomes the FooBar class imported from microservices/link/foo_bar
    """

    def __new__(cls, **kwargs):
        return MicroserviceDynamicLinkImport.by_string(cls.__name__, **kwargs)
