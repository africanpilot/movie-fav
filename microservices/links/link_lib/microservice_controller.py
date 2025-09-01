# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import ast
import os

from ariadne import load_schema_from_path
from ariadne.asgi import GraphQL
from ariadne.contrib.federation import FederatedObjectType, make_federated_schema
from fastapi import FastAPI
from graphql.error.graphql_error import GraphQLError
from link_lib.microservice_dynamic_link import MicroserviceDynamicLinkImport
from link_lib.microservice_generic_model import GenericLinkModel
from link_controller.controller_api import get_public_models, get_private_models, get_public_routes_to_load, get_private_routes_to_load
from link_models import enums
from ariadne import EnumType
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware


class ApolloTypes:
    types = {}

    @staticmethod
    def get(type):
        if type not in ApolloTypes.types:
            ptr = FederatedObjectType(type)
            ApolloTypes.types[type] = ptr
        return ApolloTypes.types[type]


class ControllerToApolloArbitraryStaticTypeDef(GenericLinkModel):
    def __init__(self):
        super().__init__()

        self._registered_type_defs = []

    def _load_registered_type_def(self, type_defs: list, relative_path, camel):
        abs_path = os.path.abspath(relative_path)
        if not os.path.isdir(abs_path):
            self.log.critical(f"No such file: {abs_path}")
            exit(1)

        kwargs = {"links": False, "log": False, "type_decorator": False}
        obj = MicroserviceDynamicLinkImport.fork(relative_path, camel, **kwargs)

        type_defs.append(obj.get_type_defs())

    def _load_registered_type_defs(self, type_defs):
        for path, camel in self._registered_type_defs:
            self._load_registered_type_def(type_defs, path, camel)

    def register_type_def(self, relative_path, camel):
        self._registered_type_defs.append((relative_path, camel))


class ControllerToApollo(ControllerToApolloArbitraryStaticTypeDef):
    def __init__(self, schema_type: enums.SchemaTypeEnum = enums.SchemaTypeEnum.PUBLIC, microservice: str = None):
        super().__init__()
        self._models_to_load = []
        self._api_models_dir = []
        self._query_load_context_skeleton = {}
        self._schema_type = schema_type
        self._directories_to_load = []
        self._microservice = microservice or self.name

    def set_models_to_load(self, model_list):
        self._models_to_load = self._models_to_load + model_list
        if self._schema_type == enums.SchemaTypeEnum.PUBLIC:
            self._models_to_load = self._models_to_load + get_public_models()
            
        if self._schema_type == enums.SchemaTypeEnum.PRIVATE:
            self._models_to_load = self._models_to_load + get_private_models()
        
    def set_api_models_dir(self, dir_list):
        self._api_models_dir = dir_list
        
    def _load_enums(self):
        return [
            EnumType(name, cls)
            for name, cls in enums.__dict__.items()
            if isinstance(cls, type) 
            and hasattr(cls, 'is_gql') 
            and cls.is_gql
        ]

    def _load_graphql_model(self, camel, query_load_context):
        return MicroserviceDynamicLinkImport.fork(query_load_context["directories"], camel, **query_load_context)

       
    def _set_query_load_context_skeleton(self):
        self._directories_to_load = [
            f"../../../{self._microservice}/src/api/gql/public/",
            "../../../../links/link_api/gql/public/",
        ] + [f"../../../{ms}/src/api/gql/public/" for ms in self.enabled_microservices]
        
        if self._schema_type == enums.SchemaTypeEnum.PRIVATE:
            self._directories_to_load = self._directories_to_load + [
                f"../../../{self._microservice}/src/api/gql/private/",
                "../../../../links/link_api/gql/private/",
            ]  + [f"../../../{ms}/src/api/gql/private/" for ms in self.enabled_microservices]
        
        self._query_load_context_skeleton = {
            "directories": self._directories_to_load,
            "log": self.log,
            "type_decorator": "dummy",
            "apollotypes": ApolloTypes,
        }
        

    def get_graphql_schema(self):
        """
        QUERY DEFINITIONS
        """
        type_defs = []

        # Clear Apollo types to avoid conflicts between schema creations
        ApolloTypes.types.clear()

        self._load_registered_type_defs(type_defs)

        self._set_query_load_context_skeleton()

        for camel in self._models_to_load:
            model = self._load_graphql_model(camel, self._query_load_context_skeleton)
            if hasattr(model, "get_type_defs"):
                type_defs.append(model.get_type_defs())
            model.load_defs()

        bindable_types = ApolloTypes.types.values()
        
        type_defs.append(str(load_schema_from_path("../../../../links/link_models/gql/public/")))
        
        if self._microservice != "monxt":
            type_defs.append(str(load_schema_from_path("../../src/models/gql/public/")))
        
        if self._microservice == "monxt":
            for ms in self.enabled_microservices:
                type_defs.append(str(load_schema_from_path(f"../../../{ms}/src/models/gql/public/")))

        if self._schema_type == enums.SchemaTypeEnum.PRIVATE:
            type_defs.append(str(load_schema_from_path("../../../../links/link_models/gql/private/")))
            
            if self._microservice != "monxt":
                type_defs.append(str(load_schema_from_path("../../src/models/gql/private/")))
            
            if self._microservice == "monxt":
                for ms in self.enabled_microservices:
                    type_defs.append(str(load_schema_from_path(f"../../../{ms}/src/models/gql/private/")))

        return make_federated_schema(type_defs, *bindable_types, self._load_enums())


class ControllerToFastApi(GenericLinkModel):
    def __init__(self, public_schema=None, private_schema=None, public_routes=None, private_routes=None):
        super().__init__()
        self._public_schema = public_schema
        self._private_schema = private_schema
        self._public_routes = public_routes
        self._private_routes = private_routes

        
    def my_format_error(self, error: GraphQLError, debug: bool = False) -> dict:
        # if debug:
        #     return format_error(error, debug)
        try:
            return ast.literal_eval(str(error.message))
        except Exception:
            return dict(
                success=False,
                code=400,
                version=1.0,
                message=error.args[0],
            )

    def get_graphql(self, schema):
        return GraphQL(
            schema,
            logger="ControllerToApollo",
            debug=True if os.environ.get("APP_DEFAULT_ENV", "prod") != "prod" else False,
            error_formatter=self.my_format_error,
        )

    def get_fastapi(self):
        if not self._public_schema and self._private_schema:
            raise ValueError("A public or private graphql schema is required")
        
        app = FastAPI()
                
        if self._public_schema:
            app.mount("/graphql", self.get_graphql(self._public_schema))
        
        if self._private_schema:
            app.mount("/internal/graphql", self.get_graphql(self._private_schema))

        # add method for adding rest routes
        # TODO: revisit this method
        app.add_middleware(SessionMiddleware, secret_key=os.getenv("APP_SECRET_KEY"))
        
        # origins = [
        #     "https://localhost",
        #     "http://localhost",
        #     "http://localhost:3000",
        #     "http://localhost:8000",
        # ]

        # app.add_middleware(
        #     CORSMiddleware,
        #     allow_origins=origins,
        #     allow_credentials=True,
        #     allow_methods=["*"],
        #     allow_headers=["*"],
        # )

        
        if get_public_routes_to_load():
           for route in get_public_routes_to_load():
                app.include_router(MicroserviceDynamicLinkImport.fork(["../../../../links/link_api/rest/public/"], route).execute())
                
        if get_private_routes_to_load():
           for route in get_private_routes_to_load():
                app.include_router(MicroserviceDynamicLinkImport.fork(["../../../../links/link_api/rest/private/"], route).execute())
 
        if self._public_routes:
            for route in self._public_routes:
                app.include_router(MicroserviceDynamicLinkImport.fork([
                    "../../src/api/rest/public/",
                    "../../../../links/link_api/rest/public/",
                ] + [f"../../../{ms}/src/api/rest/public/" for ms in self.enabled_microservices], route).execute())

        if self._private_routes:
            for route in self._private_routes:
                app.include_router(MicroserviceDynamicLinkImport.fork([
                    "../../src/api/rest/private/",
                    "../../../../links/link_api/rest/private/",
                ] + [f"../../../{ms}/src/api/rest/private/" for ms in self.enabled_microservices], route).execute())

        return app
