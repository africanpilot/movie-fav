# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.


def get_public_models():
    return [
        "DebugQuery",
        "DebugMutation",
    ]


def get_private_models():
    return [
        "GetLoginQuery",
        "RedisDeleteMutation",
    ]


def get_public_routes_to_load():
    return ["LinkBaseRouter"]


def get_private_routes_to_load():
    return []
