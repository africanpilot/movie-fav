# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from functools import cached_property

from link_domain.imdb_helper import ImdbHelper
from link_domain.imdb_ng import ImdbNg
from link_lib.microservice_request import LinkRequest


class LinkDomain(LinkRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @cached_property
    def imdb_helper(self):
        return ImdbHelper()

    @cached_property
    def imdb_ng_helper(self):
        return ImdbNg()
