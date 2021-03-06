# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from general import General
from sqlalchemy.sql import text
from imdb import IMDb

from os import path
from typing import Union

# from colorama import Fore, Back, Style

class Lib:
    
    def __init__(self, **kwargs):
        self.gen = General()
        self.TOP_N = 3
        self.ia = IMDb()
        super().__init__(**kwargs)
        
    def get_movie_info_set(self) -> list:
        return self.ia.get_movie_infoset()
    
    def get_top_movies(self) -> list:
        return self.ia.get_top250_movies()
    
    def get_popular_movies(self) -> list:
        return self.ia.get_popular100_movies()

    def search_movie_by_title(self, search: str) -> list:
        return self.ia.search_movie(search)

    def get_movie_by_id(self, imdbId: str) -> dict:
        return self.ia.get_movie(imdbId)
    
    def url_clean(self, url: str) -> str:
        if url:
            base, ext = path.splitext(url)
            url_filter = url.split('@')[0] + '@' * url.count('@')
            return url_filter.split('._V1_')[0] + ext
        return url

    def get_movie_info(self, imdbId: str, data: dict) -> dict:
        return {
            "movie_imdb_info_imdb_id": imdbId,
            "movie_imdb_info_title": data.get('title'),
            "movie_imdb_info_cast": [{"name": item["name"], "image": self.url_clean(self.ia.get_person(item.getID()).get("headshot"))} for item in data.get("cast")[:5]] if data.get("cast") else [],
            "movie_imdb_info_year": data.get('year'),
            "movie_imdb_info_directors": [item["name"] for item in data.get("directors")] if data.get("directors") else [],
            "movie_imdb_info_genres": data.get('genres'),
            "movie_imdb_info_countries": data.get('countries'),
            "movie_imdb_info_plot": data.get('plot')[0] if data.get('plot') else "",
            "movie_imdb_info_cover": self.url_clean(data.get('cover')),
        }
    
    def check_imdb_in_db(self, ids: Union[str,int], db: object) -> list[dict]:
        list_ids = self.gen.check_input_list(ids)
        sql = text(f"""
            SELECT movie_imdb_info_id,movie_imdb_info_imdb_id
            FROM movie_imdb_info
            WHERE movie_imdb_info_imdb_id IN({list_ids});
        """)
        return self.gen.list_sql_response(db=db, sql=sql)
    
    def check_fav_in_db(self, ids: Union[str,int], db: object) -> list[dict]:
        list_ids = self.gen.check_input_list(ids)
        sql = text(f"""
            SELECT movie_fav_info_imdb_id
            FROM movie_fav_info
            WHERE movie_fav_info_imdb_id IN({list_ids});
        """)
        return self.gen.list_sql_response(db=db, sql=sql)
    
    def check_fav_by_user(self, ids: Union[str,int], db: object, userId: Union[str,int]) -> list[dict]:
        list_ids = self.gen.check_input_list(ids)
        list_user = self.gen.check_input_list(userId)
        sql = text(f"""
            SELECT movie_fav_info_imdb_id
            FROM movie_fav_info
            WHERE movie_fav_info_imdb_id IN({list_ids})
            AND movie_fav_info_user_id IN ({list_user});
        """)
        return self.gen.list_sql_response(db=db, sql=sql)
    
    def movie_modify(self, ids: Union[str,int], data: dict) -> str:
        
        total_sql = ""

        # request values 
        request_key, request_val = self.gen.request_fields(data)
        request_val_list = request_val.split(",")
               
        for i,item in enumerate(request_key.split(",")):
            if "movie_fav_info" in item:
                sql = text(f"""
                    UPDATE movie_fav_info SET {item} = {request_val_list[i]}
                    WHERE movie_fav_info.movie_fav_info_id = {ids};
                """)
                total_sql+=str(sql)                                           
        return total_sql
    
    def movie_delete(self, ids: Union[str,int], db: object) -> str:
        total_sql = ""

        list_ids = self.gen.check_input_list(ids)
        
        sql = text(f"""
            SELECT *
            FROM movie_fav_info
            WHERE movie_fav_info.movie_fav_info_id IN ({list_ids});
        """)
        response = self.gen.list_sql_response(db=db, sql=sql)

        for item in response:
            # request values 
            request_key, request_val = self.gen.request_fields(item)
            
            sql = text(f"""
                INSERT INTO movie_archive({request_key})
                VALUES({request_val});
            """)
            total_sql+=str(sql)
            
        delete_sql = text(f"""                           
            DELETE 
            FROM movie_fav_info
            WHERE movie_fav_info.movie_fav_info_id IN ({list_ids});

            {total_sql}
        """)
        
        return delete_sql
    
    def movie_add_imdb(self, imdb_ids: list[str]) -> str:
        total_sql = ""
        for imdbId in imdb_ids:
                    
            # get imdb info
            self.gen.log.info(f"""Adding imdbId: {imdbId}""")
            movie_search_info = self.get_movie_by_id(imdbId=imdbId)
            movie_payload = self.get_movie_info(imdbId, movie_search_info)

            # request values 
            request_key_imdb,request_val_imdb = self.gen.request_fields(data=movie_payload)
            
            sql = text(f"""
                INSERT INTO movie_imdb_info(movie_imdb_info_id,{request_key_imdb})
                VALUES(nextval('movie_imdb_info_sequence'),{request_val_imdb});
            """)
            total_sql+=str(sql)
            
        return total_sql
    
    def _sql_db_join_types(self, sqlType: str=None) -> str:
        if sqlType == "MovieFavResponse":
            sql = """ 
                FROM movie_fav_info
                INNER JOIN movie_imdb_info ON movie_imdb_info_id = movie_fav_info.movie_fav_info_imdb_info_id
            """
        elif sqlType == "MovieImdbResponse":
            sql = """
                FROM movie_imdb_info
            """
        elif sqlType == "MovieImdbFavResponse":
            sql = """
                FROM movie_imdb_info
                LEFT JOIN movie_fav_info ON movie_fav_info_imdb_info_id = movie_imdb_info.movie_imdb_info_id
            """
        else:
            sql = """ 
                FROM movie_fav_info
                INNER JOIN movie_imdb_info ON movie_imdb_info_id = movie_fav_info.movie_fav_info_imdb_info_id
            """
        return sql
            
    def _filter_sql(self, db: object, cols: str, dbJoinTpye: str="", pageInfo: dict={}, filterInput: dict={}, oneQuery: str="") -> tuple[list, dict]:
        
        # set None to empty
        pageInfo = {} if pageInfo is None else pageInfo
        filterInput = {} if filterInput is None else filterInput
    
        # pagination techniques
        pagination_by_page_sql = ""
        pagination_by_id_sql = ""
        limit_info_sql = ""
        filter_by_sql = ""
        order_by = pageInfo["orderBy"] if "orderBy" in pageInfo and pageInfo["orderBy"] else "desc"
        sort_by = pageInfo["sortBy"] if "sortBy" in pageInfo and pageInfo["sortBy"] else "1"
        rows = 5
        filter_index = "WHERE"
        
        if pageInfo:
            rows = pageInfo["first"] if "first" in pageInfo and pageInfo["first"] else rows
            limit_sql = text(f"""LIMIT {rows}""")
            limit_info_sql+=str(limit_sql)
            if "pageNumber" in pageInfo and pageInfo["pageNumber"]:
                page = pageInfo["pageNumber"]
                limit_info_sql = ""
                sql = text(f"""
                    OFFSET ({page}-1)*{rows}
                    FETCH NEXT {rows} ROWS ONLY
                """)
                pagination_by_page_sql+=str(sql)
            elif "minId" in pageInfo and pageInfo["minId"]:
                minId = pageInfo["minId"]
                sql = text(f"""
                    {filter_index} {sort_by} < {minId}
                """)
                pagination_by_id_sql+=str(sql)
                filter_index = "AND"
            elif "maxId" in pageInfo and pageInfo["maxId"]:
                maxId = pageInfo["maxId"]
                sql = text(f"""
                    {filter_index} {sort_by} > {maxId}
                """)
                pagination_by_id_sql+=str(sql)
                filter_index = "AND"
                
        # Get db and join information
        db_join_sql = self._sql_db_join_types(sqlType=dbJoinTpye)
        
        # resolve for filter options
        if filterInput:
            list_keys = list(filterInput.keys())
            for filterKey in list_keys:
                filterVal = filterInput[filterKey]
                filterVal = self.gen.check_input_list(filterVal)
                sql = text(f"""
                    {filter_index} {filterKey} IN ({filterVal})
                """)
                filter_by_sql+=str(sql)
                if filter_index == "WHERE":
                    filter_index = "AND"
        
        # Final SQL query  
        sql = text(f"""
            {oneQuery}
                 
            SELECT {cols},COUNT(*) OVER() AS page_info_count
            {db_join_sql}
            {filter_by_sql}
            {pagination_by_id_sql}
            ORDER BY {sort_by} {order_by}
            {pagination_by_page_sql}
            {limit_info_sql}
        """)
        
        # self.gen.log.info(f"Filter sql: {sql}")
        response = self.gen.list_sql_response(db=db, sql=sql)
        page_info = {k: v for k, v in response[0].items() if k == "page_info_count"} if response else {}
        return response,page_info
    
    ### Response ----------------------------------------------------------------------------------------------------------------
    
    def movie_fav_response(self, info: object, db: object, filterInput: dict, oneQuery: str="", pageInfo: dict={}) -> dict:
        
        # Get columns to retrive
        list_movie_fav_cols = self.gen.convert_to_db_cols(info=info, first=["result"], exclude=["movie_search_info"])
        list_search_cols = self.gen.convert_to_db_cols(info=info, first=["movie_search_info"], exclude=["movie_fav_info"])
        list_search_sql = f""",row_to_json((SELECT d FROM (SELECT {list_search_cols}) d)) AS movie_search_info""" if list_search_cols else ""
        list_cols = list_movie_fav_cols + list_search_sql
        
        # exe filter sql
        result,page_info = self._filter_sql(db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="MovieFavResponse", cols=list_cols)
        return self.gen.success_response(result=result, pageInfo=page_info)
    
    def movie_imdb_response(self, info: object, db: object, pageInfo: dict={}, filterInput: dict={}, oneQuery: str="", userId: Union[str,int]=None) -> dict:
        list_im_cols = self.gen.convert_to_db_cols(info=info, first=["result"], exclude=["movie_fav_info"])
        list_fav_cols = self.gen.convert_to_db_cols(info=info, first=["movie_fav_info"], exclude=[])
        list_fav_sql = f""",row_to_json((SELECT d FROM (SELECT {list_fav_cols}) d)) AS movie_fav_info""" if list_fav_cols else ""
        list_cols = list_im_cols + "," + list_fav_cols + list_fav_sql if list_fav_cols else list_im_cols
        dbJoinTpye = "MovieImdbResponse"
        
        # add the custom movie_imdb_info_user_added column when needed
        if "movie_imdb_info_user_added" in list_cols and userId:
            list_data = list_cols.split(",")
            list_data.remove("movie_imdb_info_user_added")
            list_imdb_cols = self.gen.convert_input_items(list_data)
            
            list_ids = self.gen.check_input_list(userId)
            list_search_sql = f"""
                ,EXISTS (
                    SELECT movie_fav_info_id 
                    FROM movie_fav_info 
                    WHERE movie_fav_info.movie_fav_info_user_id IN({list_ids})
                    AND movie_fav_info.movie_fav_info_imdb_info_id = movie_imdb_info.movie_imdb_info_id
                ) AS movie_imdb_info_user_added
            """
            list_cols = list_imdb_cols + list_search_sql
            
        if list_fav_cols:
            
            # check if user has fav
            check_user_fav = self.check_fav_by_user(ids=filterInput["movie_imdb_info_imdb_id"], db=db, userId=userId)
            if check_user_fav:
                filterInput.update({"movie_fav_info_user_id": userId})
            
            dbJoinTpye = "MovieImdbFavResponse"
            
        # exe filter sql
        result,page_info = self._filter_sql(db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye=dbJoinTpye, cols=list_cols)
        return self.gen.success_response(result=result, pageInfo=page_info)


#################### For Tests ###################
 
    def movie_fav_response_for_tests(self, db: object, cols: str, filterInput: dict, oneQuery: str="", pageInfo: dict={}) -> dict:
        
        # exe filter sql
        result,page_info = self._filter_sql(db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="MovieFavResponse", cols=cols)
                
        # remove page_info_count
        result = self.gen.remove_keys(data=result, exclude=["page_info_count"])
        
        return self.gen.success_response(result=result, pageInfo=page_info)
    
    def movie_imdb_response_for_tests(self, db: object, cols: str, filterInput: dict={}, oneQuery: str="", pageInfo: dict={}) -> dict:
      
        # exe filter sql
        result,page_info = self._filter_sql(db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="MovieImdbResponse", cols=cols)
        
        # remove page_info_count
        result = self.gen.remove_keys(data=result, exclude=["page_info_count"])
        
        return self.gen.success_response(result=result, pageInfo=page_info)
   
    