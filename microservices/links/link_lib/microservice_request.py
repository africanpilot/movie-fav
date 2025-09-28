# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Union

import jwt
from graphql import FragmentDefinitionNode, FragmentSpreadNode, GraphQLResolveInfo
from link_config import config
from link_lib.microservice_response import LinkResponse
from link_lib.microservice_to_redis import LinkRedis
from link_models.enums import AccountRegistrationEnum, AccountRoleEnum, AccountStatusEnum, ServiceNameEnum
from pydantic import BaseModel


class TokenPayload(BaseModel):
    account_info_id: int
    account_company_id: int
    account_store_id: int
    service_name: ServiceNameEnum
    registration: AccountRegistrationEnum
    user_status: AccountStatusEnum
    user_role: AccountRoleEnum
    iat: datetime
    exp: datetime


class LinkRequest(LinkRedis, LinkResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_service_from_header(self, info: GraphQLResolveInfo) -> str:
        headers = dict(info.context["request"]["headers"])
        service_name = headers.get(b"service")
        if not service_name:
            return None
        if not isinstance(service_name, bytes):
            return None
        return service_name.decode()

    def check_service_authorized(
        self, info: GraphQLResolveInfo, services: list[ServiceNameEnum] = None
    ) -> ServiceNameEnum:
        services = services or [
            ServiceNameEnum.MOVIEFAV,
            ServiceNameEnum.THEATER,
        ]

        service_name = self.get_service_from_header(info)
        if service_name not in [s.value for s in services]:
            self.http_401_unauthorized_response(msg=f"Invalid service name: {service_name}")

        return ServiceNameEnum(service_name)

    def token_gen(
        self,
        account_info_id: Union[int, str],
        service: ServiceNameEnum,
        account_company_id: Optional[int] = None,
        account_store_id: Optional[int] = None,
        hr: int = 336,
        email: bool = False,
        reg: AccountRegistrationEnum = AccountRegistrationEnum.NOT_COMPLETE,
        status: AccountStatusEnum = AccountStatusEnum.ACTIVE,
        user_role: AccountRoleEnum = AccountRoleEnum.GUEST,
    ) -> str:
        issue_date = datetime.now()
        header = {"alg": "HS256", "typ": "JWT"}
        secret = os.environ["APP_DEFAULT_EMAIL_KEY"] if email else os.environ["APP_DEFAULT_ACCESS_KEY"]

        payload = {
            "account_info_id": account_info_id,
            "account_company_id": account_company_id,
            "account_store_id": account_store_id,
            "service_name": service.value if hasattr(service, "value") else service,
            "registration": reg.value if hasattr(reg, "value") else reg,
            "user_status": status.value if hasattr(status, "value") else status,
            "user_role": user_role.value if hasattr(user_role, "value") else user_role,
            "iat": issue_date,
            "exp": issue_date + timedelta(hours=hr),
        }

        return jwt.encode(headers=header, payload=payload, key=secret, algorithm="HS256")

    def get_query_request(
        self,
        selections,
        fragments: Dict[str, FragmentDefinitionNode] = None,
        finalData: list = None,
        lastNest: int = None,
        currNode: str = None,
        rootNode: str = None,
    ) -> list[tuple]:
        if finalData is None:
            lastNest = 0
            finalData = []
            currNode = None
            rootNode = None

        rootNode = currNode

        for i in range(len(selections)):
            # get the node or field name
            curr_selection = selections[i]
            name = curr_selection.name.value

            if isinstance(curr_selection, FragmentSpreadNode):
                curr_selection = fragments[name]

            # selection check tells us if there are nested fields for this node
            selectionsCheck = curr_selection.selection_set

            # set current node as we continue to go down nested levels
            # do not set the fragment node for our use case
            currNode = name if selectionsCheck and curr_selection.kind != "fragment_definition" else currNode

            # no need to append the original rootnode information or nodes we know have nests
            if rootNode and not selectionsCheck:
                finalData.append((rootNode, name, lastNest))

            # continue if current field does not have a nest
            if not selectionsCheck:
                continue

            # current field has nested levels, execute recursion
            selectionsData = curr_selection.selection_set.selections
            self.get_query_request(
                selections=selectionsData,
                fragments=fragments,
                finalData=finalData,
                lastNest=lastNest + 1,
                currNode=currNode,
                rootNode=rootNode,
            )

        return finalData

    def convert_to_db_cols(
        self, root_node: str, query_context: list[tuple] = None, info: GraphQLResolveInfo = None, exclude: list = None
    ) -> str:
        if not query_context and not info:
            self.http_400_bad_request_response(
                "Must provide the graphql resolver info or use the LinkRequest.get_query_request function"
            )

        if not query_context and info:
            query_context = self.get_query_request(selections=info.field_nodes, fragments=info.fragments)

        exclude = exclude if exclude else ["__typename"]

        return [node[1] for node in query_context if node[0] == root_node and node[1] not in exclude]

    def convert_to_db_cols_with_attr(
        self,
        resultObject,
        root_node: str,
        query_context: list[tuple] = None,
        info: GraphQLResolveInfo = None,
        exclude: list = None,
    ):
        return [
            getattr(resultObject, v)
            for v in self.convert_to_db_cols(
                info=info, root_node=root_node, query_context=query_context, exclude=exclude
            )
        ]

    def strip_token(self, header: str) -> str:
        bearer, _, token = header.partition(" ")
        if bearer != "Bearer":
            self.http_401_unauthorized_response(msg="Invalid token")
        return token

    def get_token_from_header(self, info: GraphQLResolveInfo) -> str:
        if config.APP_DEFAULT_ENV in {"prod", "dev"}:
            header = info.context["request"].headers
            token = str(header.get("authorization")).encode()
        else:
            header = {k: v for k, v in info.context["request"]["headers"].items()}
            token = header.get(b"authorization")

        if not token:
            self.http_401_unauthorized_response(msg="Invalid token")

        if not isinstance(token, bytes):
            self.http_401_unauthorized_response(msg="Invalid token")

        return token.decode("utf-8")

    def get_token(self, info: GraphQLResolveInfo) -> str:
        return self.strip_token(self.get_token_from_header(info))

    def decode_token(self, info: GraphQLResolveInfo, email: bool = False) -> TokenPayload:
        secret = os.environ["APP_DEFAULT_EMAIL_KEY"] if email else os.environ["APP_DEFAULT_ACCESS_KEY"]
        try:
            token_decode = jwt.decode(jwt=self.get_token(info), key=secret, algorithms=["HS256"])
            return TokenPayload(
                account_info_id=token_decode["account_info_id"],
                account_company_id=token_decode["account_company_id"],
                account_store_id=token_decode["account_store_id"],
                service_name=ServiceNameEnum(token_decode["service_name"]),
                registration=AccountRegistrationEnum(token_decode["registration"]),
                user_status=AccountStatusEnum(token_decode["user_status"]),
                user_role=AccountRoleEnum(token_decode["user_role"]),
                iat=token_decode["iat"],
                exp=token_decode["exp"],
            )
        except jwt.DecodeError:
            self.http_401_unauthorized_response(msg="Invalid token")
        except jwt.ExpiredSignatureError:
            self.http_401_unauthorized_response(msg="Invalid token")
        except Exception as e:
            self.http_401_unauthorized_response(msg=f"Invalid token: {e}")

    def check_current_token_assigned(self, token, account: int):
        redis_result = self.account_redis_engine.get(f"""account_me_token:{account}""")
        if not redis_result or redis_result.decode("utf-8") != token:
            self.http_401_unauthorized_response(msg="Invalid token, please login")

    # Token and service Validation Process
    def general_validation_process(
        self,
        info: GraphQLResolveInfo,
        email: bool = False,
        reg: bool = False,
        service_list: list[ServiceNameEnum] = [
            ServiceNameEnum.MOVIEFAV,
            ServiceNameEnum.THEATER,
        ],
        company: bool = False,
        guest: bool = False,
        roles: list[AccountRoleEnum] = None,
    ) -> TokenPayload:

        # get service name
        service_name = self.check_service_authorized(info, service_list)

        # validate token
        token_decode = self.decode_token(info, email)

        # validate guest
        if not guest and (
            not token_decode.account_info_id
            or token_decode.account_info_id == 0
            or token_decode.user_role == AccountRoleEnum.GUEST
        ):
            self.http_401_unauthorized_response("Unauthorized guest access")

        # validate role access
        if roles and token_decode.user_role not in roles:
            self.http_401_unauthorized_response("Unauthorized role access")

        # validate company
        if company and (
            not token_decode.account_company_id
            or token_decode.account_company_id == 0
            or token_decode.user_role in [AccountRoleEnum.GUEST, AccountRoleEnum.CUSTOMER]
        ):
            self.http_401_unauthorized_response("Unauthorized company access")

        # FIXME: needs to account for more than one device
        # self.check_current_token_assigned(self.get_token(info), token_decode.account_info_id)

        # verify service name in request matches the one in token
        if token_decode.service_name != service_name:
            self.http_499_token_required_response(msg="Invalid token service name")

        # verify active user
        if token_decode.user_status != AccountStatusEnum.ACTIVE:
            self.http_401_unauthorized_response(msg="Account not active")

        # only when not checking email token
        if not email and not reg:

            # verify registration status
            if token_decode.registration == AccountRegistrationEnum.NOT_COMPLETE:
                self.http_401_unauthorized_response(msg="Please complete registration first")

            if token_decode.registration in [AccountRegistrationEnum.WAITING, AccountRegistrationEnum.COMPLETE]:
                self.http_401_unauthorized_response(msg="Registration is pending approval")

        return token_decode

    def check_store_access(self, account_stores: Optional[list[int]], store_ids: list[int]) -> None:
        if not account_stores or not all([store_id in account_stores for store_id in store_ids]):
            self.http_401_unauthorized_response("Unauthorized store access")
