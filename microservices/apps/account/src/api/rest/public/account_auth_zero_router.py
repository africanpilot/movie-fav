# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import json

from urllib.parse import quote_plus, urlencode
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter

from account.src.app_lib import config


class AccountAuthZeroRouter:
    def __init__(self, **kwargs):
        pass
    
    @property
    def prefix(self) -> str:
        return "/v1.0/account"

    def execute(self):
        router = APIRouter(
            prefix=self.prefix,
            # tags=["items"],
            responses={404: {"description": "Not found"}},
        )
        oauth = OAuth()
        oauth.register(
            "auth0",
            client_id=config.AUTH0_CLIENT_ID,
            client_secret=config.AUTH0_CLIENT_SECRET,
            client_kwargs={
                "scope": "openid profile email",
            },
            server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration',
        )

        @router.get('/')
        async def home(request: Request):
            user = request.session.get('user')
            if user:
                data = json.dumps(user, indent=4)
                html = (
                    f'<pre>{data}</pre>'
                    f'<a href="/v1.0/account/logout">logout</a>'
                )
                return HTMLResponse(html)
            return HTMLResponse(f'<a href="/v1.0/account/login">login</a>')

        @router.get('/callback')
        async def callback(request: Request):
            try:
                token = await oauth.auth0.authorize_access_token(request)
            except OAuthError as error:
                return HTMLResponse(f'<h1>{error.error}</h1>')
            else:
                user = token.get('userinfo')
                if user:
                    request.session['user'] = dict(user)
                return RedirectResponse(url='/')

        @router.get('/login')
        async def login(request: Request):
            return await oauth.auth0.authorize_redirect(
                request, redirect_uri=request.url_for('callback')
            )

        @router.get('/logout')
        async def logout(request: Request):
            request.session.pop('user', None)
            return RedirectResponse(
                "https://"
                + config.AUTH0_DOMAIN
                + "/v2/logout?"
                + urlencode(
                    {
                        "returnTo": request.url_for("home"),
                        "client_id": config.AUTH0_CLIENT_ID,
                    },
                    quote_via=quote_plus,
                )
            )

        return router
