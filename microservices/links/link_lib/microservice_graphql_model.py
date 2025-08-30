# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


from link_lib.microservice_generic_model import GenericLinkModel


class GenericModelGraphQL(GenericLinkModel):
    def __init__(self, **kwargs):
        self.log = kwargs["log"]
        self.type_decorator = kwargs["type_decorator"]
        if "apollotypes" in kwargs:
            self.ApolloTypes = kwargs["apollotypes"]


class GraphQLModel(GenericModelGraphQL):
    def get_type_defs(self):
        return self.type_defs if hasattr(self, "type_defs") else ""
