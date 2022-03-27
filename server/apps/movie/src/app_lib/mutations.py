from ariadne import MutationType
from typing import Union

from api.movie_create_mutation import MovieCreateMutation
from api.movie_modify_mutation import MovieModifyMutation
from api.movie_delete_mutation import MovieDeleteMutation
from api.movie_imdb_populate_mutation import MovieImdbPopulateMutation

class Mutations:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    mutation = MutationType()

    @mutation.field("movieCreate")
    def resolve_movie_create(_, info: object, movieInput: dict) -> dict:
        return MovieCreateMutation.movie_create_mutation(_, info, movieInput)
    
    @mutation.field("movieModify")
    def resolve_movie_modify(_, info: object, movieInput: dict) -> dict:
        return MovieModifyMutation.movie_modify_mutation(_, info, movieInput)
    
    @mutation.field("movieDelete")
    def resolve_movie_delete(_, info: object, movie_fav_info_id: Union[str,int]) -> dict:
        return MovieDeleteMutation.movie_delete_mutation(_, info, movie_fav_info_id)
    
    @mutation.field("movieImdbPopulate")
    def resolve_movie_imdb_populate(_, info: object, pageInfo: dict) -> dict:
        return MovieImdbPopulateMutation.movie_imdb_populate_mutation(_, info, pageInfo)