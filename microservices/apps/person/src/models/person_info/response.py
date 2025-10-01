# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional

from graphql import GraphQLResolveInfo
from link_lib.microservice_request import LinkRequest
from link_models.base import BaseResponse, PageInfoInput
from person.src.models.person_info import PersonInfo, PersonInfoBase, PersonInfoFilterInput, PersonInfoPageInfoInput
from sqlmodel import Session


class PersonInfoBaseResponse(PersonInfoBase):
    id: Optional[int] = None


class PersonInfoResponse(BaseResponse):
    result: Optional[list[PersonInfoBaseResponse]] = None


class PersonInfoResponses(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def person_info_cols(
        self, info: GraphQLResolveInfo = None, query_context=None, root_node: str = "result"
    ) -> list[PersonInfo]:
        return self.convert_to_db_cols_with_attr(
            resultObject=PersonInfo, info=info, query_context=query_context, root_node=root_node
        )

    def person_response(
        self,
        info: GraphQLResolveInfo,
        db: Session,
        pageInfo: PersonInfoPageInfoInput = PageInfoInput(),
        filterInput: PersonInfoFilterInput = None,
        filterInputExtra: list = None,
        extraCols: list[PersonInfo] = None,
        query_context: list[tuple] = None,
        baseRootNode: str = "result",
    ) -> PersonInfoResponse:
        # check nulls
        extraCols = extraCols or []
        filterInputExtra = filterInputExtra or []

        if not query_context:
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

        person_info = self.person_info_cols(query_context=query_context, root_node=baseRootNode)
        total_list_cols = set(person_info + extraCols)
        total_filter = set(self.get_filter_info_in(filterInput, PersonInfo) + filterInputExtra)

        # exe filter sql
        result, page_info = self.filter_sql(
            db=db,
            pageInfo=pageInfo,
            filterInput=total_filter,
            cols=total_list_cols,
            baseObject=PersonInfo,
        )

        return self.success_response(result=result, pageInfo=page_info, nullPass=True, resultObject=PersonInfoResponse)
