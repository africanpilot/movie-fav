# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from typing import Union
from celery import Task

from link_lib.saga_framework import saga_step_handler
from link_models.enums import ImportProviderTypeEnum
from link_models.messaging import SHOWS_IMPORT_SAGA_RESPONSE_QUEUE, shows_import_message as message
from link_domain.pyratebay import PyratebayLib, Torrent
from shows.src.controller.controller_worker import worker
from shows.src.domain.lib import ShowsLib


@worker.task(bind=True, name=message.TASK_NAME)
@saga_step_handler(response_queue=SHOWS_IMPORT_SAGA_RESPONSE_QUEUE)
def shows_import_task(self: Task, saga_id: int, payload: dict) -> Union[dict, None]:
    request_data = message.ShowsImportMessage(**payload)
    lib = ShowsLib()

    try:
        with lib.get_session("psqldb_shows") as db:
            remaining_shows = [ shows for shows in lib.get_no_download_urls(db) if shows.title is not None]
            if request_data.download_type == "1080p":
                remaining_shows = [ shows for shows in remaining_shows if not shows.download_1080p_url]
                
            if request_data.download_type == "720p":
                remaining_shows = [ shows for shows in remaining_shows if not shows.download_720p_url]
                
            if request_data.download_type == "480p":
                remaining_shows = [ shows for shows in remaining_shows if not shows.download_480p_url]
            
            lib.log.info(f"remaining_shows: {len(remaining_shows)}")
            sql_query = []
            
            for i,shows in enumerate(remaining_shows[:request_data.page]):
                
                lib.log.info(f"{i} -- Searching for {shows.title} in {shows.imdb_id}")
                
                magnet_url = lib.get_magnet_url(shows.title, request_data.download_type, shows.season, shows.episode)
                
                if magnet_url:
                    if request_data.download_type == "1080p":
                        fields = dict(download_1080p_url=magnet_url)
                    elif request_data.download_type == "720p":
                        fields = dict(download_720p_url=magnet_url)
                    else:
                        fields = dict(download_480p_url=magnet_url)
                    
                    sql_query.append(lib.shows_info_update_imdb(db, shows.imdb_id, False, **fields))
                
            for r in sql_query:
                db.exec(r)
            db.commit()
            db.close()
        
        lib.redis_delete_shows_info_keys()

    except Exception as e:
        raise lib.http_400_bad_request_response(
            f"Failed to get shows {request_data.download_type} for saga id {saga_id} -- {e}"
        )
            
    return None