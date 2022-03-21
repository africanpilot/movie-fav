from ariadne import MutationType
from ariadne.contrib.federation import FederatedObjectType
from app_lib.lib import Lib


class Federations:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    lib = Lib()
    
    movieFavInfo = FederatedObjectType("MovieFavInfo")
    accountInfo = FederatedObjectType("AccountInfo")
    
    # add to export list
    federation = [movieFavInfo, accountInfo]
    
    @accountInfo.field("account_info_to_movie_fav_info")
    def resolve_account_info_to_movie_fav_info(representation, *_):
        lib = Lib()      
        if representation["account_info_id"]:
            with lib.gen.db.get_engine("psqldb_movie").connect() as db:
                return lib.movie_fav_response(info=_[0], db=db, filterInput={"movie_fav_info_user_id": representation["account_info_id"]})
        return lib.gen.success_response(nullPass=True, result=[])