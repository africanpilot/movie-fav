# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Optional
from link_models.enums import OrderByEnum
from pydantic import BaseModel


class GeneralResponse(BaseModel):
	code: int = 0
	success: bool = False
	message: str = "Error not handled"
	version: str = "1.0"


class PageInfo(BaseModel):
	page_info_count: Optional[int] = 0


class ConstBase(BaseModel):
	response: GeneralResponse
	pageInfo: PageInfo

class BaseResponse(ConstBase):
	result: list = None


class PageInfoInput(BaseModel):
	first: int = 5
	pageNumber: Optional[int] = None
	minId: Optional[int] = None
	maxId: Optional[int] = None
	orderBy: OrderByEnum = OrderByEnum.DESC
	refresh: bool = False
