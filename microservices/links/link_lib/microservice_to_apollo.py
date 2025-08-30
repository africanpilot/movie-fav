# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import logging
import os
from multiprocessing import cpu_count

import uvicorn
from gunicorn import glogging
from gunicorn.app.base import BaseApplication
from link_lib.microservice_generic_model import GenericLinkModel, microservice_name
from link_lib.microservice_logger import MicroserviceLogger


class ProductionApplication(BaseApplication):
    def _number_of_workers(self):
        return (cpu_count() * 2) + 1

    def _setup_logging(self):
        log_format = MicroserviceLogger.format_gunicorn(microservice_name())
        glogging.Logger.error_fmt = log_format
        glogging.Logger.access_fmt = log_format
        glogging.Logger.syslog_fmt = log_format
        glogging.Logger.datefmt = ""

    def __init__(self, app, options={}):
        self._setup_logging()
        required_options = {
            "bind": "%s:%s" % ("0.0.0.0", str(os.environ.get("APP_DEFAULT_PORT", 8000))),
            "workers":int(os.environ.get("GUNICORN_WORKERS", self._number_of_workers())),
            "worker_class": "uvicorn.workers.UvicornWorker",
            "preload": True,
            "log-file": "-",
            "timeout": 60,
        }
        required_options.update(options)
        self.options = required_options
        self.application = app
        super().__init__()

    def load_config(self):
        """
        Method Required by Gunicorn base class
        """
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """
        Method required by Gunicorn base class
        """
        return self.application


class DevelopmentApplication(GenericLinkModel):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        uvicorn.run(
            "app:app",
            host=self.host,
            port=int(self.port),
            reload=True,
            debug=True,
            reload_dirs=[
                "../../src/",
                "../../../../links/"
            ] + [f"../../../{ms}/src/" for ms in self.enabled_microservices],
        )


class MicroserviceToApollo:
    def __init__(self, app, port: int = None):
        self.app = app
        self.port = port

    def run(self):
        host = "0.0.0.0"
        port = self.port or str(os.environ.get("APP_DEFAULT_PORT", 8000))

        if os.environ["APP_DEFAULT_ENV"] == "prod":
            options = {"bind": "%s:%s" % (host, port)}
            ProductionApplication(app=self.app, options=options).run()
        else:
            DevelopmentApplication(host, port).run()
