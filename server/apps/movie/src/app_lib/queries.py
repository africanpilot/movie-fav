from ariadne import QueryType
from api.movie_fav_query import MovieFavQuery
from api.movie_search_query import MovieSearchQuery
from api.movie_popular_query import MoviePopularQuery

class Queries:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    query = QueryType()
    
    @query.field("movieFav")
    def resolve_movie_fav(_, info: object, pageInfo: object={}, filterInput: object={}) -> dict:
        return MovieFavQuery.movie_fav_query(_, info, pageInfo, filterInput)
    
    @query.field("movieSearch")
    def resolve_movie_search(_, info: object, pageInfo: object={}, filterInput: object={}) -> dict:
        return MovieSearchQuery.movie_search_query(_, info, pageInfo, filterInput)
    
    @query.field("moviePopular")
    def resolve_movie_popular(_, info: object, pageInfo: object={}) -> dict:
        return MoviePopularQuery.movie_popular_query(_, info, pageInfo)