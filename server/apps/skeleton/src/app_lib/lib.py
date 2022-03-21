from general import General
from sqlalchemy.sql import text
from colorama import Fore, Back, Style


class Lib:
    
    def __init__(self, **kwargs):
        self.gen = General()
        super().__init__(**kwargs)
    
    def _sql_db_join_types(self, sqlType=None):
        if sqlType == "ExampleResponse":
            sql = """ 
            """
        else:
            sql = """"
            """
        return sql
            
    def _filter_sql(self, info, db, cols, pageInfo={}, filterInput={}, oneQuery="", dbJoinTpye=""):
        
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
    
    def example_response(self, info, db, pageInfo, filterInput, oneQuery=""):
        # list_cols = self.gen.convert_to_db_cols(info=info, first=["result"], exclude=[""])

        # # exe filter sql
        # result,page_info = self._filter_sql(info=info, db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, dbJoinTpye="ExampleResponse", cols=list_cols)
        # return self.gen.success_response(result=result, pageInfo=page_info)

        return "hello"