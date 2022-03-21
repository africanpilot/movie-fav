# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib

class MovieSearchQuery:

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def movie_search_query(self, info, pageInfo, filterInput):
        
        lib = Lib()
        movie_list = []
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        # get imdb data based on search title
        if filterInput["search_type"] == "search_title":
            movies = lib.search_movie_by_title(search=filterInput["search_value"])

            # get movie info limit return
            limit = pageInfo["first"] if "first" in pageInfo and pageInfo["first"] else 5
            for i,movie in enumerate(movies):
                movie_payload = lib.get_movie_info(movie.getID(), movie)
                movie_list.append(movie_payload)
                if i+1 == limit:
                    break
                
        # get imdb data based on search title
        if filterInput["search_type"] == "search_imdb_id":
            movie_search_info = lib.get_movie_by_id(imdbId=filterInput["search_value"])
            movie_payload = lib.get_movie_info(filterInput["search_value"], movie_search_info)
            movie_list.append(movie_payload)
            
        return lib.gen.success_response(result=movie_list, pageInfo={"page_info_count":len(movie_list)})