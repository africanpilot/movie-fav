import os
import link
import gunicorn.app.base

from ariadne import load_schema_from_path
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import make_federated_schema
from app_lib.mutations import Mutations
from app_lib.queries import Queries
from app_lib.federations import Federations
from os.path import dirname, realpath, basename
from multiprocessing import cpu_count

type_defs = load_schema_from_path("schema.graphql")
objects = Federations.federation + [Queries.query, Mutations.mutation]
schema = make_federated_schema(type_defs, objects)
application = GraphQL(schema)

APP_PORT_NAME = "APP_PORT_" + os.path.basename(dirname(dirname(dirname(realpath(__file__))))).upper()


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    
    def _number_of_workers(self):
        return (cpu_count() * 2) + 1

    def __init__(self, app, options={}):
        required_options = {
            'bind': '%s:%s' % ('0.0.0.0', str(os.environ[APP_PORT_NAME])),
            'workers': self._number_of_workers(),
            "worker_class": "uvicorn.workers.UvicornWorker",
            "preload": True,
            'log-file' : '-',
            'timeout': 0,
        }
        options.update(required_options)
        self.options = options
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    
    if os.environ['MOVIE_FAV_ENV'] in ["local","test"]:
        import uvicorn
        uvicorn.run("app:application", 
                    host="0.0.0.0", port=int(os.environ[APP_PORT_NAME]), 
                    reload=True, 
                    reload_dirs=[
                        "../../src/api",
                        "../../src/app_lib",
                        "../../src/test",
                        "../../../../links/",
                    ])
    else:
        StandaloneApplication(app=application).run()