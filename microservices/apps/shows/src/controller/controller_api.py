# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from link_lib.microservice_controller import ControllerToApollo
from link_models.enums import SchemaTypeEnum


class APIController(ControllerToApollo):
    """
    List of the class models for each query type.
    These classes must be in the ../api/ or '../../../../links/link_api/' directories
    """

    public_models_to_load = [
        "ShowsInfoQuery",
        "ShowsFederations",
        "ShowsEpisodeQuery",
        "ShowsEpisodeUpdateMutation",
    ]
    
    private_models_to_load = [
        "ShowsInfoPopulateMutation",
        "ShowsResetPopularMutation",
        "ShowsInfoUpdateMutation",
        "ShowsImportMutation",
    ]

    public_routes_to_load = []

    private_routes_to_load = []

    def __init__(self, schema_type: SchemaTypeEnum = SchemaTypeEnum.PUBLIC, microservice: str = "shows"):
        super().__init__(schema_type)
        self._schema_type = schema_type
        self._microservice = microservice

        self.set_models_to_load(self.public_models_to_load)
        
        if self._schema_type == SchemaTypeEnum.PRIVATE:
            self.set_models_to_load(self.private_models_to_load)


class APISchema:
    public_schema = APIController(schema_type=SchemaTypeEnum.PUBLIC).get_graphql_schema()
    private_schema = APIController(schema_type=SchemaTypeEnum.PRIVATE).get_graphql_schema()
    public_routes = APIController.public_routes_to_load
    private_routes = APIController.private_routes_to_load
