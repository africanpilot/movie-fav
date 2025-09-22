# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


import json
from typing import Union

from link_lib.microservice_general import GeneralJSONEncoder, LinkGeneral
from link_models.base import BaseResponse, GeneralResponse, PageInfo, PageInfoInput
from sqlalchemy import select
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql.selectable import Select
from sqlmodel import asc, desc, func


class HTTPException(Exception):
    pass


class LinkResponse(LinkGeneral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_filter_info(self, filterInput: dict, obj: object):
        return [getattr(obj, k) == v for k, v in filterInput.items()]

    def get_filter_info_in(self, filterInput: object, obj: object, exclude: dict = None):
        return (
            [
                getattr(obj, k).in_(v) if isinstance(v, list) else getattr(obj, k) == v
                for k, v in filterInput.model_dump(exclude_unset=True, exclude=exclude).items()
            ]
            if filterInput
            else []
        )

    def get_json_row(self, cols: list[object], name: str):
        return select(func.row_to_json(select(*cols).subquery().table_valued())).label(name)

    def get_json_row_response(self, cols: list[object], name: str):
        if not cols:
            return []
        return [self.get_json_row(cols, name)]

    def query_cols(self, cols: list) -> Select:
        return select(*cols, func.count().over().label("page_info_count"))

    def get_page_info_count_over(self, result: list):
        if not result:
            return {}

        first_result = result[0]
        if first_result is None:
            return {}

        try:
            # Handle SQLAlchemy Row objects or dict-like objects
            if hasattr(first_result, "_asdict"):
                # SQLAlchemy Row object
                result_dict = first_result._asdict()
            elif hasattr(first_result, "__dict__"):
                # Object with __dict__
                result_dict = first_result.__dict__
            else:
                # Try to convert to dict
                result_dict = dict(first_result)

            return {k: v for k, v in result_dict.items() if k == "page_info_count"}
        except (TypeError, AttributeError, ValueError) as e:
            self.log.warning(f"Error processing page info count: {e}, result[0]: {first_result}")
            return {}

    def join_tables(self, sql_query: Select, dbJoinType: list[dict] = None) -> Select:
        if dbJoinType:
            for j in dbJoinType:
                sql_query = sql_query.join_from(**j)
        return sql_query

    def query_filter(self, sql_query: Select, filterInput: list) -> Select:
        if filterInput:
            sql_query = sql_query.where(*filterInput)
        return sql_query

    def paginate_by_page_number(self, sql_query: Select, pageInfo: PageInfoInput) -> Select:
        if pageInfo.pageNumber:
            sql_query = sql_query.offset((pageInfo.pageNumber - 1) * pageInfo.first)
        return sql_query

    def sort_by_sql(self, pageInfo, baseObject):
        if hasattr(pageInfo, "sortBy") and pageInfo.sortBy:
            return [getattr(baseObject, i.value) for i in pageInfo.sortBy]
        return [baseObject.id]

    def get_table_cols(self, obj: object):
        return [getattr(obj, k) for k in obj.__fields__.keys()]

    def convert_sql_response_to_dict(self, result) -> list[dict]:
        if not result:
            return []

        converted_result = []
        for r in result:
            if hasattr(r, "_asdict"):
                # For namedtuple-like objects
                converted_result.append(r._asdict())
            elif hasattr(r, "_mapping"):
                # For SQLAlchemy Row objects with _mapping attribute
                converted_result.append(dict(r._mapping))
            elif hasattr(r, "keys") and callable(r.keys):
                # For Row objects that have keys() method
                converted_result.append({key: r[key] for key in r.keys()})
            elif isinstance(r, dict):
                # Already a dictionary
                converted_result.append(r)
            else:
                # Fallback: try to convert directly
                try:
                    converted_result.append(dict(r))
                except (TypeError, ValueError) as e:
                    # If conversion fails, convert to string representation
                    self.log.warning(f"Could not convert row to dict: {r}, error: {e}")
                    converted_result.append({"raw_data": str(r)})

        return converted_result

    def convert_response(self, response) -> dict:
        redis_conv = response.model_dump() if hasattr(response, "model_dump") else response.dict()
        redis_conv.update(dict(result=self.convert_sql_response_to_dict(redis_conv["result"])))
        return redis_conv

    def create_array_subquery(self, obj, name: str):
        return select(func.to_json(func.array_agg(func.row_to_json(obj)))).label(name)

    def order_by_sql(self, pageInfo):
        return desc if pageInfo.orderBy.value == "desc" else asc

    def order_and_sort(self, sql_query: Select, baseObject, pageInfo):
        order_by = self.order_by_sql(pageInfo)
        sort_by = self.sort_by_sql(pageInfo, baseObject)
        return sql_query.order_by(order_by(*sort_by))

    def get_all(self, db: Connection, sql_query: Select) -> tuple[list, PageInfo]:
        # self.log.debug(f"sql_query: {sql_query}")
        # execute result and pageInfo
        result = db.execute(sql_query).all()
        page_info = PageInfo(**self.get_page_info_count_over(result))
        # self.log.debug(f"result query: {self.convert_sql_response_to_dict(result)}")
        return result, page_info

    def filter_sql(
        self,
        db: Connection,
        baseObject,
        cols: list = None,
        pageInfo=None,
        dbJoinType: list = None,
        filterInput: list = None,
        oneQuery=None,
        query_all: bool = True,
    ) -> tuple[list, PageInfo]:
        # check nulls
        pageInfo = pageInfo or PageInfoInput()

        # set all columns to return
        sql_query = self.query_cols(cols) if cols else oneQuery

        # resolve all joins
        sql_query = self.join_tables(sql_query, dbJoinType)

        # apply filters
        sql_query = self.query_filter(sql_query, filterInput)

        # sort and order results
        sql_query = self.order_and_sort(sql_query, baseObject, pageInfo)

        # paginate by page
        sql_query = self.paginate_by_page_number(sql_query, pageInfo)

        # limit the rows returned
        sql_query = sql_query.limit(pageInfo.first)

        # self.log.info(f"sql_query: {sql_query}")
        if query_all:
            return self.get_all(db, sql_query)

        return sql_query

    def general_response_model(self, resultObject):
        return resultObject(
            response=GeneralResponse(),
            pageInfo=PageInfo(),
            result=None,
        )

    def update_general_response(self, response: GeneralResponse, resultObject):
        payload = self.general_response_model(resultObject)
        payload.response = response
        return payload

    def success_response(
        self,
        resultObject,
        result: Union[list, dict] = None,
        pageInfo: PageInfo = None,
        nullPass: bool = False,
        resultBase=None,
    ) -> dict:
        if not result and not nullPass:
            self.http_404_not_found_response(msg="expecting data but nothing was returned")

        payload = self.update_general_response(GeneralResponse(code=200, success=True, message="Success"), resultObject)
        payload.pageInfo = pageInfo

        if result and resultBase:
            result = [resultBase(**item._asdict()) for item in result]

        payload.result = result
        return payload

    def http_400_bad_request_response(self, msg: str = None) -> dict:
        raise HTTPException(
            json.dumps(
                self.update_general_response(
                    GeneralResponse(code=400, message=f"http_400_bad_request: {msg}"), BaseResponse
                ).model_dump(),
                cls=GeneralJSONEncoder,
            )
        )

    def http_401_unauthorized_response(self, msg: str = None) -> dict:
        raise HTTPException(
            json.dumps(
                self.update_general_response(
                    GeneralResponse(code=401, message=f"http_401_unauthorized: {msg}"), BaseResponse
                ).model_dump(),
                cls=GeneralJSONEncoder,
            )
        )

    def http_403_forbidden_response(self, msg: str = None) -> dict:
        raise HTTPException(
            json.dumps(
                self.update_general_response(
                    GeneralResponse(code=403, message=f"http_403_forbidden: {msg}"), BaseResponse
                ).model_dump(),
                cls=GeneralJSONEncoder,
            )
        )

    def http_404_not_found_response(self, msg: str = None) -> dict:
        raise HTTPException(
            json.dumps(
                self.update_general_response(
                    GeneralResponse(code=404, message=f"http_404_not_found: {msg}"), BaseResponse
                ).model_dump(),
                cls=GeneralJSONEncoder,
            )
        )

    def http_498_invalid_token_response(self, msg: str = None) -> dict:
        raise HTTPException(
            json.dumps(
                self.update_general_response(
                    GeneralResponse(code=498, message=f"http_498_invalid_token: {msg}"), BaseResponse
                ).model_dump(),
                cls=GeneralJSONEncoder,
            )
        )

    def http_499_token_required_response(self, msg: str = None) -> dict:
        raise HTTPException(
            json.dumps(
                self.update_general_response(
                    GeneralResponse(code=499, message=f"http_499_token_required: {msg}"), BaseResponse
                ).model_dump(),
                cls=GeneralJSONEncoder,
            )
        )

    def http_500_internal_server_error(self, msg: str = None) -> dict:
        raise HTTPException(
            json.dumps(
                self.update_general_response(
                    GeneralResponse(code=500, message=f"http_500_internal_server_error: {msg}"), BaseResponse
                ).model_dump(),
                cls=GeneralJSONEncoder,
            )
        )
