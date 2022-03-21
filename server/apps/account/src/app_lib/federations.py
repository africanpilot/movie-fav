from ariadne import MutationType
from ariadne.contrib.federation import FederatedObjectType
from app_lib.lib import Lib


class Federations:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    lib = Lib()

    # add to export list
    federation = []