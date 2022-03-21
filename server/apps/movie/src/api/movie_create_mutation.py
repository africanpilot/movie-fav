# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from app_lib.lib import Lib
from sqlalchemy.sql import text
from colorama import Fore

class MovieCreateMutation:
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movie_create_mutation(self, info, movieInput):
        
        lib = Lib()
        
        # Token and service Validation Process
        general_validation_payload, token_decode = lib.gen.general_validation_process(info)
        if general_validation_payload != "success":
            return general_validation_payload
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            
            # check if imdb id is already in the db if not then create record
            total_sql=""
            imdbId = movieInput["movie_fav_info_imdb_id"]
            imdb_exists = lib.check_imdb_in_db(ids=imdbId, db=db)
            fav_exists = lib.check_fav_in_db(ids=imdbId, db=db)
            
            if not fav_exists:
                if not imdb_exists:
                    lib.gen.log.info(f"Movie does not exist adding imdbId: {imdbId}")
                    # get imdb info
                    movie_search_info = lib.get_movie_by_id(imdbId=imdbId)
                    movie_payload = lib.get_movie_info(imdbId, movie_search_info)
                    # lib.gen.log.debug(f"Movie payload: {movie_payload}")
                    
                    # request values 
                    request_key_imdb,request_val_imdb = lib.gen.request_fields(data=movie_payload)
                    
                    sql = text(f"""
                        INSERT INTO movie_imdb_info(movie_imdb_info_id,{request_key_imdb})
                        VALUES(nextval('movie_imdb_info_sequence'),{request_val_imdb});
                    """)
                    total_sql+=str(sql)
                    movieInput.update({"movie_fav_info_imdb_info_id": "currval('movie_imdb_info_sequence')"})
                else:
                    movieInput.update({"movie_fav_info_imdb_info_id": imdb_exists[0]["movie_imdb_info_id"]})
                
                # request values
                movieInput.update({"movie_fav_info_user_id": token_decode["user_id"]})
                request_key,request_val = lib.gen.request_fields(data=movieInput)
                
                # get results
                sql = text(f"""                   
                    INSERT INTO movie_fav_info(movie_fav_info_id,{request_key})
                    VALUES(nextval('movie_fav_info_sequence'),{request_val});
                """)
                total_sql+=str(sql)
            else:
                lib.gen.log.info(f"Movie already in db: {imdbId}")
            
            
            lib.gen.log.info(f"total_sql: {total_sql}")   
            # response
            return lib.movie_fav_response(info=info, db=db, pageInfo={}, filterInput={"movie_fav_info_imdb_id":imdbId}, oneQuery=total_sql)