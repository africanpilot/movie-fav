# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from general import General
from sqlalchemy.sql import text
from typing import Union
from datetime import datetime

# from colorama import Fore, Back, Style

class Lib:
    
    def __init__(self, **kwargs):
        self.gen = General()
        super().__init__(**kwargs)
        
    def get_user_credentials(self, db: object, login: str) -> dict:
        sql = text(f"""
            SELECT account_info_id,account_info_email,account_info_password,account_info_status
            ,account_info_verified_email,account_info_registration_status
            FROM account_info
            WHERE account_info.account_info_email = '{login}'
        """)
        result = self.gen.list_sql_response(db=db, sql=sql)
        return result[0] if result else {}
        
    def verify_login_exists(self, db: object, login: str):
        try:
            sql = text(f"""
                SELECT account_info_id,account_info_status,account_info_verified_email
                FROM account_info 
                WHERE account_info.account_info_email = '{login}'
            """)
            return True if db.execute(sql).fetchall() else False
        except Exception as e:
            self.gen.log.critical(f"verify_login_exists: No response = {e}")
            return "DB"
        
    def account_create(self, data: object) -> str:
        
        # account_info
        password_hash = self.gen.hash_password(data["password"]).decode("utf-8")
        dateModified = str(datetime.utcnow())

        sql = text(f"""
            INSERT INTO account_info(account_info_id,account_info_email,account_info_password,account_info_registered_on) 
            VALUES(nextval('account_info_sequence'),'{data["login"]}','{password_hash}','{dateModified}');

            INSERT INTO account_contact(account_contact_info_id) 
            VALUES(currval('account_info_sequence'));
        """)
        
        return sql
    
    def account_modify(self, id: Union[int,str], data: dict) -> str:
        
        total_sql = ""
        
        # request values 
        request_key, request_val = self.gen.request_fields(data)
        request_val_list = request_val.split(",")
               
        for i,item in enumerate(request_key.split(",")):
            if "account_info" in item:
                sql = text(f"""
                    UPDATE account_info SET {item} = {request_val_list[i]}
                    WHERE account_info.account_info_id = {id};
                """)
                total_sql+=str(sql)
            if "account_contact" in item:
                sql = text(f"""
                    UPDATE account_contact SET {item} = {request_val_list[i]}
                    WHERE account_contact.account_contact_info_id = {id};
                """)
                total_sql+=str(sql)
        # self.gen.log.debug(f"total_sql: {total_sql}")                                             
        return total_sql
    
    def account_delete(self, ids: Union[str,list,int], db: object) -> str:
        total_sql = ""

        list_ids = self.gen.check_input_list(ids)
        
        sql = text(f"""
            SELECT *
            FROM account_info
            INNER JOIN account_contact ON account_contact.account_contact_info_id = account_info.account_info_id
            WHERE account_info.account_info_id IN ({list_ids});
        """)
        user_response = self.gen.list_sql_response(db=db, sql=sql)

        for user in user_response:
            # request values 
            request_key, request_val = self.gen.request_fields(user)
            
            sql = text(f"""
                INSERT INTO account_archive({request_key})
                VALUES({request_val});
            """)
            total_sql+=str(sql)
            
        user_delete_sql = text(f"""
                                         
            DELETE 
            FROM account_info
            WHERE account_info.account_info_id IN ({list_ids});

            {total_sql}
            
            UPDATE account_archive SET account_info_status = 'DELETED'
            WHERE account_archive.account_info_id IN ({list_ids}); 
        """)
        
        return user_delete_sql
    
    def update_user_logout_info(self, ids: Union[str,int]) -> str:
        logout_date = str(datetime.utcnow())
        sql = text(f"""
            UPDATE account_info SET account_info_last_logout_date = '{logout_date}'
            WHERE account_info.account_info_id = {ids};
        """)
        
        return sql
    
    def delete_user(self, email: str) -> str:
        sql = text(f"""
            DELETE 
            FROM account_info
            WHERE account_info.account_info_email = '{email}';
        """)
        
        return sql
    
    def update_email_confirmed(self, ids: Union[str,int]) -> str:
        sql = text(f"""
            UPDATE account_info SET (account_info_verified_email,account_info_registration_status,account_info_status) = (True,'APPROVED','ACTIVE')
            WHERE account_info.account_info_id = {ids};
        """)
        return sql
    
    def get_password_expire_date(self, db: object, ids: Union[str,int]) -> list:
        list_ids = self.gen.check_input_list(ids)
        sql = text(f"""
            SELECT account_info_forgot_password_expire_date
            FROM account_info
            WHERE account_info.account_info_id IN({list_ids});
        """)
        result = self.gen.list_sql_response(db=db, sql=sql)
        return result[0] if result else []
    
    def _sql_db_join_types(self, sqlType: str=None) -> str:
        if sqlType == "AccountAuthenticationResponse":
            sql = """
                FROM account_info
                INNER JOIN account_contact ON account_contact.account_contact_info_id = account_info.account_info_id 
            """
        else:
            sql = """
                FROM account_info
                INNER JOIN account_contact ON account_contact.account_contact_info_id = account_info.account_info_id
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
                
        # check cols
        cols = cols if cols else "1"
                      
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
        return response, page_info
    
    ### Response ----------------------------------------------------------------------------------------------------------------
    
    def account_authentication_response(self, info: object, db: object, token: str, status: str, filterInput: dict={}, oneQuery: str="", extraCols: list=[]) -> dict:
        
        # get columns to return
        list_cols_client = self.gen.convert_to_db_cols(info=info, first=["accountInfo"], exclude=[])
        list_cols = ",".join(list(set(list_cols_client.split(",") + extraCols)))
        
        # exe filter sql
        result, page_info = self._filter_sql(db=db, cols=list_cols, filterInput=filterInput, oneQuery=oneQuery)
        auth_result = {
            "authenticationToken": token,
            "authenticationTokenType": "ACCESSTOKEN",
            "registrationStatus": status,
            "accountInfo": result,
        }
        
        return self.gen.success_response(result=auth_result, pageInfo=page_info)
    
    def account_response(self, info: object, db: object, pageInfo: dict={}, filterInput: dict={}, oneQuery: str="", extraCols: list=[]) -> dict:
        
        # get columns to return
        list_cols_client = self.gen.convert_to_db_cols(info=info, first=["result"], exclude=[])
        list_cols = ",".join(list(set(list_cols_client.split(",") + extraCols)))

        # exe filter sql
        result, page_info = self._filter_sql(db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, cols=list_cols)
        
        return self.gen.success_response(result=result, pageInfo=page_info)


#################### For Tests ###################

    def account_response_for_test(self, db: object, cols: str, pageInfo: dict={}, filterInput: dict={}, oneQuery: str="") -> dict:

        # exe filter sql
        result, page_info = self._filter_sql(db=db, pageInfo=pageInfo, filterInput=filterInput, oneQuery=oneQuery, cols=cols)
        
        # remove page_info_count
        result = self.gen.remove_keys(data=result, exclude=["page_info_count"])
        
        return self.gen.success_response(result=result, pageInfo=page_info)