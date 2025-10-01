# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from link_models.enums import AccountRoleEnum
from person.src.domain.lib import PersonLib
from person.src.models.person_info import PersonInfo, PersonInfoCreateInput, PersonInfoResponse


class PersonImportMutation(GraphQLModel, PersonLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("personImport")
        def resolve_person_import(_, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None) -> PersonInfoResponse:

            self.general_validation_process(
                info, roles=[AccountRoleEnum.ADMIN, AccountRoleEnum.COMPANY, AccountRoleEnum.MANAGER]
            )

            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()

            with self.get_session("psqldb_person") as db:
                all_saga_state_to_import = self.person_saga_state_read.get_remaining_person_sagas_to_ingest(
                    db, pageInfo.first
                )
                person_info_all = [PersonInfoCreateInput(**saga.payload) for saga in all_saga_state_to_import]
                self.person_info_create.person_info_create_imdb(db, person_info_all)

                self.redis_delete_person_info_keys()

                all_person_ids = [p.imdb_id for p in person_info_all]
                response = self.person_info_response.person_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInputExtra=[PersonInfo.imdb_id.in_(all_person_ids)],
                    query_context=query_context,
                )

                db.close()

            return response
