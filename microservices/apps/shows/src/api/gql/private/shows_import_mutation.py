# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


from graphql import GraphQLResolveInfo
from link_lib.microservice_controller import ApolloTypes
from link_lib.microservice_graphql_model import GraphQLModel
from link_models.base import PageInfoInput
from link_models.enums import AccountRoleEnum
from shows.src.domain.lib import ShowsLib
from shows.src.models.shows_info import ShowsInfo, ShowsInfoCreateInput, ShowsInfoResponse


class ShowsImportMutation(GraphQLModel, ShowsLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_defs(self):
        mutation = ApolloTypes.get("Mutation")

        @mutation.field("showsImport")
        def resolve_shows_import(_, info: GraphQLResolveInfo, pageInfo: PageInfoInput = None) -> ShowsInfoResponse:

            self.general_validation_process(
                info, roles=[AccountRoleEnum.ADMIN, AccountRoleEnum.COMPANY, AccountRoleEnum.MANAGER]
            )

            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)
            pageInfo = PageInfoInput(**pageInfo) if pageInfo else PageInfoInput()

            with self.get_session("psqldb_shows") as db:
                all_saga_state_to_import = self.shows_saga_state_read.get_remaining_shows_sagas_to_ingest(
                    db, pageInfo.first
                )
                shows_info_all = [ShowsInfoCreateInput(**saga.payload) for saga in all_saga_state_to_import]
                self.shows_info_create.shows_info_create_imdb(db, shows_info_all)

                # clear old popular ids
                all_popular_ids = self.imdb_helper.get_charts_imdbs("tvmeter")

                sql_query = []
                sql_query.append(self.shows_info_update.shows_info_update_popular_id(db, commit=False, popular_id=None))

                # update popular order
                for i, item in enumerate(all_popular_ids):
                    sql_query.append(
                        self.shows_info_update.shows_info_update_by_imdb_id(
                            db=db, imdbId=item, commit=False, popular_id=i + 1
                        )
                    )

                for query in sql_query:
                    db.exec(query)
                db.commit()

                self.redis_delete_shows_info_keys()
                self.redis_delete_shows_episode_keys()

                response = self.shows_info_response.shows_response(
                    info=info,
                    db=db,
                    pageInfo=pageInfo,
                    filterInputExtra=[ShowsInfo.imdb_id.in_(all_popular_ids)],
                    query_context=query_context,
                )

                db.close()

            return response
