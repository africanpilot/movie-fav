# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import link # noqa: F401

from link_lib.microservice_controller import ControllerToFastApi
from link_lib.microservice_to_apollo import MicroserviceToApollo
from shows.src.controller.controller_api import APISchema


app = ControllerToFastApi(APISchema.public_schema, APISchema.private_schema, APISchema.public_routes, APISchema.private_routes).get_fastapi()

if __name__ == "__main__":
    MicroserviceToApollo(app).run()
