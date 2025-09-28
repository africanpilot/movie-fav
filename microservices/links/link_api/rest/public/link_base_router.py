# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse


class LinkBaseRouter:
    def __init__(self, **kwargs):
        pass

    @property
    def prefix(self) -> str:
        return ""

    def execute(self):
        router = APIRouter(
            prefix=self.prefix,
            responses={404: {"description": "Not found"}},
        )

        @router.get("/")
        async def home(request: Request):
            return HTMLResponse('<a href="/docs">documentation</a>')

        @router.get("/health")
        async def health(request: Request):
            return HTMLResponse("<p>OK</p>")

        return router
