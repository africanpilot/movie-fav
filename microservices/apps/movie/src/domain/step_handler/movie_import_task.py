# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task

from link_lib.saga_framework import saga_step_handler
from link_models.messaging import MOVIE_IMPORT_SAGA_RESPONSE_QUEUE, movie_import_message as message
from movie.src.controller.controller_worker import worker
from movie.src.domain.lib import MovieLib


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=MOVIE_IMPORT_SAGA_RESPONSE_QUEUE)
def movie_import_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.MovieImportMessage(**payload)
    lib = MovieLib()

    try:
        with lib.get_session("psqldb_movie") as db:
            remaining_movies = [ movie for movie in lib.get_no_download_urls(db) if movie.title is not None]
            if request_data.download_type == "1080p":
                remaining_movies = [ movie for movie in remaining_movies if not movie.download_1080p_url]
                
            if request_data.download_type == "720p":
                remaining_movies = [ movie for movie in remaining_movies if not movie.download_720p_url]
                
            if request_data.download_type == "480p":
                remaining_movies = [ movie for movie in remaining_movies if not movie.download_480p_url]
            
            lib.log.info(f"remaining_movies: {len(remaining_movies)}")
            sql_query = []
            
            for i,movie in enumerate(remaining_movies[:request_data.page]):
                
                lib.log.info(f"{i} -- Searching for {movie.title} in {movie.imdb_id}")
                
                magnet_url = lib.get_magnet_url(movie.title, request_data.download_type)
                
                if magnet_url:
                    if request_data.download_type == "1080p":
                        fields = dict(download_1080p_url=magnet_url)
                    elif request_data.download_type == "720p":
                        fields = dict(download_720p_url=magnet_url)
                    else:
                        fields = dict(download_480p_url=magnet_url)
                    
                    sql_query.append(lib.movie_info_update_imdb(db, movie.imdb_id, False, **fields))
                
            for r in sql_query:
                db.exec(r)
            db.commit()
            db.close()
        
        lib.redis_delete_movie_info_keys()

    except Exception as e:
        raise lib.http_400_bad_request_response(
            f"Failed to get movie {request_data.download_type} for saga id {saga_id} -- {e}"
        )
            
    return None