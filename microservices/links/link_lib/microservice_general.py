# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import random
import string
from datetime import datetime
from enum import Enum
from json import JSONEncoder
from sqlalchemy.engine import Row

from link_lib.microservice_generic_model import GenericModel


class LinkGeneral(GenericModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fil_json_keys(self, x: dict, y: list[str]) -> dict:
        return {k: v for k, v in x.items() if k in y}

    def remove_keys(self, data: list[dict], exclude: list[str]) -> list[dict]:
        return [{k: v for k, v in d.items() if k not in exclude} for d in data]

    def rand_word_gen_range(self, start: int = 1, end: int = 30) -> str:
        return "".join(random.choice(string.ascii_lowercase) for i in range(random.randint(start, end)))

    def compose_decos(self, decos):
        def composition(func):
            for deco in reversed(decos):
                func = deco(func)
            return func

        return composition


class GeneralJSONEncoder(JSONEncoder):
    def default(self, obj):

      def default_encoder(obj):
        if isinstance(obj, Enum):
          return obj.value
        
        if isinstance(obj, set):
            return list(obj)
        
        if isinstance(obj, datetime):
          return str(obj)
        
        return None
      
      get_encoder = default_encoder(obj)
      if get_encoder is not None:
          return get_encoder
      return super().default(obj)