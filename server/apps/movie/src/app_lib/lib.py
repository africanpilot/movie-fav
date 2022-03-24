from pydantic import BaseModel
from general import General
import datetime
import requests
from bs4 import BeautifulSoup
from sqlalchemy.sql import text
from colorama import Fore, Back, Style
import time
import json
import string
from imdb import IMDb
import os

class Lib:
    
    def __init__(self, **kwargs):
        self.gen = General()
        self.TOP_N = 3
        self.ia = IMDb()
        super().__init__(**kwargs)
        
    def get_movie_info_set(self):
        return self.ia.get_movie_infoset()
    
    def get_top_movies(self):
        return self.ia.get_top250_movies()
    
    def get_popular_movies(self):
        return self.ia.get_popular100_movies()

    def search_movie_by_title(self, search):
        movies = self.ia.search_movie(search)
        return movies

    def get_movie_by_id(self, imdbId):
        get_movie_data = self.ia.get_movie(imdbId)
        return get_movie_data
    
    def url_clean(self, url):
        if url:
            base, ext = os.path.splitext(url)
            i = url.count('@')
            s2 = url.split('@')[0]
            s3 = s2 + '@' * i
            result = s3.split('._V1_')[0] + ext
            return result
        return url

    def get_movie_info(self, imdbId, data):
        payload = {
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
        return payload
    
    def check_imdb_in_db(self, ids, db):
        list_ids = self.gen.check_input_list(ids)
        sql = text(f"""
            SELECT movie_imdb_info_id,movie_imdb_info_imdb_id
            FROM movie_imdb_info
            WHERE movie_imdb_info_imdb_id IN({list_ids});
        """)
        response = self.gen.list_sql_response(db=db, sql=sql)
        return response
    
    def check_fav_in_db(self, ids, db):
        list_ids = self.gen.check_input_list(ids)
        sql = text(f"""
            SELECT movie_fav_info_imdb_id
            FROM movie_fav_info
            WHERE movie_fav_info_imdb_id IN({list_ids});
        """)
        response = self.gen.list_sql_response(db=db, sql=sql)
        return response
    
    def movie_modify(self, ids, data):
        
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
    
    def movie_delete(self, ids, db):
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
    
    def movie_add_imdb(self, imdb_ids):
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
    
    def _sql_db_join_types(self, sqlType=None):
        if sqlType == "MovieFavResponse":
            sql = """ 
                FROM movie_fav_info
                INNER JOIN movie_imdb_info ON movie_imdb_info_id = movie_fav_info.movie_fav_info_imdb_info_id
            """
        elif sqlType == "MovieImdbResponse":
            sql = """
                FROM movie_imdb_info
            """
            # INNER JOIN movie_fav_info ON movie_fav_info_imdb_info_id = movie_imdb_info.movie_imdb_info_id
        else:
            sql = """ 
                FROM movie_fav_info
                INNER JOIN movie_imdb_info ON movie_imdb_info_id = movie_fav_info.movie_fav_info_imdb_info_id
            """
        return sql
            
    def _filter_sql(self, info, db, cols, dbJoinTpye="", pageInfo={}, filterInput={}, oneQuery=""):
        
        # set None to empty
        pageInfo = {} if pageInfo is None else pageInfo
        filterInput = {} if filterInput is None else filterInput
    
        # pagination techniques
        pagination_by_page_sql = ""
        pagination_by_id_sql = ""
        limit_info_sql = ""
        filter_by_sql = ""
        order_by = pageInfo["orderBy"] if "orderBy" in pageInfo and pageInfo["orderBy"] else "desc"
        sort_by = pageInfo["sortBy"] if "sortBy" in pageInfo and pageInfo["sortBy"] else "1" # TODO: check if sort by 1 can work
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
    
    def movie_fav_response(self, info, db, filterInput, oneQuery="", pageInfo={}):
        
        # Get columns to retrive
        list_movie_fav_cols = self.gen.convert_to_db_cols(info=info, first=["result"], exclude=["movie_search_info"])
        list_search_cols = self.gen.convert_to_db_cols(info=info, first=["movie_search_info"], exclude=["movie_fav_info"])
        list_search_sql = f""",row_to_json((SELECT d FROM (SELECT {list_search_cols}) d)) AS movie_search_info""" if list_search_cols else ""
        list_cols = list_movie_fav_cols + list_search_sql
        
        # exe filter sql
        result,page_info = self._filter_sql(info=info, db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="MovieFavResponse", cols=list_cols)
        return self.gen.success_response(result=result, pageInfo=page_info)
    
    def movie_imdb_response(self, info, db, pageInfo={}, filterInput={}, oneQuery="", userId=None):
        list_cols = self.gen.convert_to_db_cols(info=info, first=["result"], exclude=["movie_fav_info"])

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
            
        # exe filter sql
        result,page_info = self._filter_sql(info=info, db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="MovieImdbResponse", cols=list_cols)
        return self.gen.success_response(result=result, pageInfo=page_info)


#################### For Tests ###################
 
    def movie_fav_response_for_tests(self, db, cols, filterInput, oneQuery="", pageInfo={}):
        
        # exe filter sql
        result,page_info = self._filter_sql(info=None, db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="MovieFavResponse", cols=cols)
                
        # remove page_info_count
        result = [{k: v for k, v in d.items() if k != "page_info_count"} for d in result]
        
        return self.gen.success_response(result=result, pageInfo=page_info)
    
    def movie_imdb_response_for_tests(self, db, cols, pageInfo={}, filterInput={}, oneQuery="", userId=None):
      
        # exe filter sql
        result,page_info = self._filter_sql(info=None, db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="MovieImdbResponse", cols=cols)
        
        # remove page_info_count
        result = [{k: v for k, v in d.items() if k != "page_info_count"} for d in result]
        
        return self.gen.success_response(result=result, pageInfo=page_info)
   
    