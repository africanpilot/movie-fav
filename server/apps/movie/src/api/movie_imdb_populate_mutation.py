# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from sqlalchemy.sql import text
from colorama import Fore

class MovieImdbPopulateMutation:
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movie_imdb_populate_mutation(self, info, pageInfo):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        # check if imdb id is already
        total_sql=""
        limit = pageInfo["first"] if "first" in pageInfo and pageInfo["first"] else 5
        movie_popular_ids = [movie.getID() for movie in lib.get_popular_movies()[:limit]]
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
        
            movie_popular_complete = [movie["movie_imdb_info_imdb_id"] for movie in lib.check_imdb_in_db(ids=movie_popular_ids, db=db)]
            movie_popular_todo = list(filter(lambda x: x not in movie_popular_complete, movie_popular_ids)) 
            
            if movie_popular_todo:
                for imdbId in movie_popular_todo:
                    
                    # get imdb info
                    lib.gen.log.info(f"""Adding imdbId: {imdbId}""")
                    movie_search_info = lib.get_movie_by_id(imdbId=imdbId)
                    movie_payload = lib.get_movie_info(imdbId, movie_search_info)
  
                    # request values 
                    request_key_imdb,request_val_imdb = lib.gen.request_fields(data=movie_payload)
                    
                    sql = text(f"""
                        INSERT INTO movie_imdb_info(movie_imdb_info_id,{request_key_imdb})
                        VALUES(nextval('movie_imdb_info_sequence'),{request_val_imdb});
                    """)
                    total_sql+=str(sql)
            else:
                lib.gen.log.info(f"Movie popular already up to date")
            
            lib.gen.log.info(f"total_sql: {total_sql}")   
            
            # response
            return lib.movie_imdb_response(info=info, db=db, pageInfo={"first": 5}, filterInput={"movie_imdb_info_imdb_id": movie_popular_ids}, oneQuery=total_sql)