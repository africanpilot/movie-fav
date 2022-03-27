# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

from logging.config import dictConfig
from config import LogConfig
from logging import getLogger

from database import DbConn
from sqlalchemy.sql import text

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from itertools import zip_longest
from json import dumps
from random import randint, choice
from string import ascii_lowercase
from re import match
from os import environ
from jwt import encode, decode, DecodeError, ExpiredSignatureError
from bcrypt import checkpw, hashpw, gensalt
from datetime import datetime, timedelta
from typing import Union

class General:
    
    def __init__(self, **kwargs):
        dictConfig(LogConfig().dict())
        self.log = getLogger("applog")
        self.db = DbConn()
        super().__init__(**kwargs)

    def convert_items(self, data: dict, list_keys: list) -> str:
        new_data = []
        for x in list_keys:
            if type(data[x]) in [str,datetime]:
                val = str(data[x])
                if val.find("currval('") != -1:
                    new_data.append(val)
                else:
                    new_data.append("'" + val.replace("'","''") + "'")

            elif type(data[x]) is list:
                list_types = []
                dicType = False
                for item in data[x]:
                    if not dicType and type(item) is dict:
                        dicType = True
                        
                    if type(item) is str:
                        list_types.append(item.replace("'","!?!?!"))
                    elif type(item) is dict:
                    
                        for key, value in item.items():
                            if item[key]:
                                item[key] = item[key].replace("'","!?!?!")
                        
                        list_types.append(dumps(item))
                    else:
                        list_types.append(item)
                
                if dicType:
                    new_data.append("ARRAY" + str(list_types) + "::json[]")   
                else:
                    new_data.append("ARRAY" + str(list_types))
        
            else:
                new_data.append(data[x])
        
        return self.convert_input_items(new_data)

    def convert_input_items(self, list_key: list) -> str:
        list_key = ",".join(map(str,list_key))
        return list_key
    
    def convert_input(self, list_key: list) -> str:
        list_val = ["'"+ x + "'" if type(x) is str else str(x) for x in list_key]
        list_val = ", ".join(list_val) 
        return list_val
    
    def check_input_list(self, ids: Union[str,int,list]) -> str:
        if type(ids) is list:
            list_ids = self.convert_input(ids)
        else:
            list_ids = "'" + str(ids) + "'" if type(ids) is str else ids
            
        return list_ids

    def list_sql_response(self, db: object, sql: str) -> list[dict]:
        response = [dict(result) for result in db.execute(sql).fetchall()]
        return response
    
    def fil_json_keys(self, x: dict, y) -> dict:
        return dict([ (i,x[i]) for i in x if i in set(y) ])
    
    def remove_keys(self, data: list[dict], exclude: list[str]) -> list[dict]:
        return [{k: v for k, v in d.items() if k not in exclude} for d in data]
    
    def request_fields(self, data: dict) -> tuple[str,str]:
        data = {k: v for k, v in data.items() if v is not None}
        data = self.remove_duplicate_keys(data=data)
        request_list_keys = list(data.keys())
        request_key = self.convert_input_items(request_list_keys)
        request_val = self.convert_items(data, request_list_keys)
        return request_key,request_val

    def get_query_request(self, selections: object, finalData: list=None, lastNest: int=None) -> list[dict]:
        if finalData == None:
            lastNest = 0
            finalData = []
        for i in range(len(selections)):
            data = selections[i].name.value
            finalData.append({data:lastNest})
            # self.log.debug(f"{i} -- finalData: {finalData}")
            selectionsCheck = selections[i].selection_set
            if not selectionsCheck:
                # self.log.debug(f"{i} -- selectionsCheck: {selectionsCheck}")
                continue
            selectionsData = selections[i].selection_set.selections
            # self.log.debug(f"{i} -- selectionsData: {selectionsData}")
            self.get_query_request(selections=selectionsData, finalData=finalData, lastNest=lastNest+1)

        return finalData
        
    def convert_to_db_cols(self, info: object, first: list, exclude: list=[]) -> str:
        exclude.append("__typename")
        response = self.get_query_request(selections=info.field_nodes)
        result = []
        
        if response:
            data = []
            start = False
            end = False
            val_num = None
            for item in response:
                if end:
                    break
                for key in item:
                    val = item[key]
                    if key in first:
                        start = True
                        val_num = val+1
                    if start and key != first and val == val_num and key not in exclude:
                        data.append(key)
            result = self.convert_input_items(data)
        return result

    def remove_duplicate_keys(self, data: dict) -> dict:
        result = {}
        for key,value in data.items():
            if value not in result.values():
                result[key] = value
        return result

    def hash_password(self, password: str) -> str:
        return hashpw(password.encode('utf8'), gensalt(int(environ['MOVIE_FAV_GEN_SALT_VALUE'])))

    def verify_hash_password(self, password: str, hashed: str) -> bool:
         return True if checkpw(password, hashed) else False
    
    def token_gen(self, id, service: str, hr: int=336, email: bool=False, reg: str="NOTCOMPLETE", status: str="ACTIVE") -> str:
        issue_date = datetime.utcnow()
        header = {'alg': "HS256",'typ': "JWT"}
        secret = environ['MOVIE_FAV_EMAIL_KEY'] if email else environ['MOVIE_FAV_ACCESS_KEY']
        payload = {
            'user_id': id,
            'service-name': service,
            'registration':reg,
            'user_status': status,
            'iat': issue_date,
            'exp': issue_date + timedelta(hours=hr)
        }
        
        return encode(headers=header,payload=payload, key=secret,algorithm="HS256")

    def get_service_from_header(self, info: object) -> str:
        return dict(info.context["request"]["headers"])[b'service-name'].decode("utf-8")

    def email_check(self, email: str) -> bool:
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return True if(match(regex, email)) else False
        
    def password_check(self, password: str) -> bool:
        regex = r"(^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?^&])[A-Za-z\d@$!%*^#?&]{8,}$)"
        return True if(match(regex, password)) else False
    
    def get_token(self, header: str) -> str:
        bearer, _, token = header.partition(' ')
        return "" if bearer != 'Bearer' else token
                
    def get_token_from_header(self, info: object) -> str:
        # user_agent = info.context["request"].get("HTTP_AUTHORIZATION", "Authorization")
        # user_agent = info.context["request"].headers["authorization"]
        # TODO: issues with syncing this up with testing env to use code above
        user_agent = dict(info.context["request"]["headers"])[b'authorization'].decode("utf-8")
        
        return self.get_token(user_agent)
    
    def token_validation(self, token: str, email: str) -> bool:
        secret = environ['MOVIE_FAV_EMAIL_KEY'] if email else environ['MOVIE_FAV_ACCESS_KEY']
        try:
            decode(jwt=token, key=secret, algorithms=["HS256"])
            return True
        except (DecodeError, ExpiredSignatureError) as e:
            self.log.critical(f"token_validation: {e}")
            return False
    
    def decode_token(self, info: object, email: bool=False) -> dict:
        secret = environ['MOVIE_FAV_EMAIL_KEY'] if email else environ['MOVIE_FAV_ACCESS_KEY']
        return decode(jwt=self.get_token_from_header(info), key=secret,algorithms=["HS256"]) 
    
    # Token and service Validation Process
    def general_validation_process(self, info: object, email: bool=False, reg: bool=False, service_list: list=["moviefav-service"]) -> tuple[dict, dict]:
             
        # validate token exists
        token = self.get_token_from_header(info)
        if not token:
            return self.http_499_token_required_response(msg="Unable to get token"), {}
        
        # get service from header
        service = self.get_service_from_header(info)
        if service not in service_list:
            return self.http_499_token_required_response(msg="Invalid service name"), {}
        
        # validate token
        valid_token = self.token_validation(token, email)
        if not valid_token:
            return self.http_498_invalid_token_response(msg="Invalid token"), {}
        
        # decode token
        token_decode = self.decode_token(info, email)

        # verify service access
        if token_decode["service-name"] != service:
            return self.http_499_token_required_response(msg="Invalid token service name"), {}

        # verify active user
        if token_decode["user_status"] != 'ACTIVE':
            return self.http_401_unauthorized_response(msg="Account not active"), {}

        # only when not checking email token
        if not email and not reg:

            # verify registration status
            if token_decode["registration"] == "NOTCOMPLETE":
                return self.http_401_unauthorized_response(msg="Please complete registration first"), {}
             
            if token_decode["registration"] in ["WAITING", "COMPLETE"]:
                return self.http_401_unauthorized_response(msg="Registration is pending approval"), {}
            
            if token_decode["registration"] not in ["NOTCOMPLETE", "WAITING", "COMPLETE", "APPROVED"]:
                return self.http_401_unauthorized_response(msg="Unknown registration"), {}
                
        return self.success_response(nullPass=True), token_decode
    
    def send_to_sendgrid(self, msg: dict, template: str) -> bool:
        if environ['MOVIE_FAV_ENV'] in ["dev", "local", "prod"]:
            # send to sendgrid
            SENDGRID_API_KEY = environ['SENDGRID_API_KEY']
            APP_ADDRESS = environ['APP_ADDRESS']
            send_to_email = msg["email"] if environ['MOVIE_FAV_EMAIL'] == 'prod' else str(environ['MOVIE_FAV_EMAIL'])
            message = Mail(
                from_email='makurichard14@gmail.com',
                to_emails=send_to_email,
            )
            
            # Template for Email verification
            if template == "VerifyEmail":
                SENDGRID_TEMPLATE_VERIFY_EMAIL_ID = 'd-6be05110f3cd4023b3b7a4bd95a42b6a'
                token = msg["token"] 
                
                if environ['MOVIE_FAV_ENV'] == 'prod':
                    link = f"https://{APP_ADDRESS}/email-confirmation?ur_token={token}"  
                else:
                    link = f"http://localhost:3000/email-confirmation?ur_token={token}"  

                message.dynamic_template_data = {
                    'Weblink': link,
                    'email': send_to_email
                }
                message.template_id = SENDGRID_TEMPLATE_VERIFY_EMAIL_ID

            # Template for Forgot Password
            if template == "ForgotPassword":
                SENDGRID_TEMPLATE_FORGOT_PASSWORD_EMAIL_ID = 'd-37ac03c4ec204abc83e84296da060677'
                token = msg["token"]
            
                if environ['MOVIE_FAV_ENV'] == 'prod':
                    link = f"https://{APP_ADDRESS}/change-password?ur_token={token}" 
                else:
                    link = f"http://localhost:3000/change-password?ur_token={token}"  
                
                message.dynamic_template_data = {'Weblink': link}
                message.template_id = SENDGRID_TEMPLATE_FORGOT_PASSWORD_EMAIL_ID

            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                sg.send(message)
                return True
            except Exception as e:
                self.log.critical(f"Sengrid Failed to send: {e}")
                return False
        return True
    
    def rand_word_gen(self) -> str:
        return ''.join(choice(ascii_lowercase) for i in range(randint(1, 30)))

    def rand_word_gen_range(self, start: int, end: int) -> str:
        return ''.join(choice(ascii_lowercase) for i in range(randint(start, end)))
    
    def batcher(self, iterable: object, n: int) -> object:
        return zip_longest(*[iter(iterable)] * n)
    
    def redis_delete_keys_pipe(self, db, search: Union[str,list], n: int=50) -> object:
        pipe = db.pipeline()
        if type(search) == str:
            search = [search]
            
        for item in search:
            for keybatch in self.batcher(db.scan_iter(item), n):
                pipe.delete(*filter(None, keybatch))
            
        return pipe
        
    def general_response_model(self) -> dict:
        return {
            "response": {
                "code": 200,
                "success": False,
                "message": "",
                "version": "1.0",
            },
            "result": [],
            "pageInfo": {}
        }
    
    def compose_decos(self, decos):
        def composition(func):
            for deco in reversed(decos):
                func = deco(func)
            return func
        return composition
    
    def update_general_response(self, data: dict) -> dict:
        payload = self.general_response_model()
        payload["response"].update(data)
        return payload
        
    def success_response(self, result=[], pageInfo: dict={}, nullPass: bool=False) -> dict:
        if not result and not nullPass:
            return self.http_404_not_found_response()
        
        payload = self.update_general_response({
            "success":True,
            "message":"Success!"
        })
        payload.update({"result":result})
        payload.update({"pageInfo":pageInfo})
        return payload
    
    def http_400_bad_request_response(self, msg: str="") -> dict:
        return self.update_general_response({
            "code":400,
            "message": f"http_400_bad_request: {msg}"
        })
    
    def http_401_unauthorized_response(self, msg: str="") -> dict:
        return self.update_general_response({
            "code":401,
            "message": f"http_401_unauthorized: {msg}"
        })
        
    def http_403_forbidden_response(self, msg: str="") -> dict:
        return self.update_general_response({
            "code":403,
            "message": f"http_403_forbidden: {msg}"
        })
    
    def http_404_not_found_response(self, msg: str="") -> dict:
        return self.update_general_response({
            "code":404,
            "message": f"http_404_not_found: {msg}"
        })
    
    def http_498_invalid_token_response(self, msg: str="") -> dict:
        return self.update_general_response({
            "code":498,
            "message": f"http_498_invalid_token: {msg}"
        })
        
    def http_499_token_required_response(self, msg: str="") -> dict:
        return self.update_general_response({
            "code":499,
            "message": f"http_499_token_required: {msg}"
        })
    
    def http_500_internal_server_error(self, msg: str="") -> dict:
        return self.update_general_response({
            "code":499,
            "message": f"http_500_internal_server_error: {msg}"
        })
    

#################### For Tests ###################

    def auth_info(self, data: dict={"id": 1, "email": False, "reg": "NOTCOMPLETE"}) -> dict:
        SERVICE = "moviefav-service"
        TOKEN = self.token_gen(id=data["id"], service=SERVICE, hr=24, reg=data["reg"], email=data["email"], status="ACTIVE")
        AUTH_TOKEN = f"Bearer {TOKEN}".encode('utf-8')
        SERVICE_NAME = f"{SERVICE}".encode('utf-8')
        DEFAULT_HEADER = { b'authorization': AUTH_TOKEN, b'service-name': SERVICE_NAME }
        CONTEXT_VALUE = { "request": {"headers": DEFAULT_HEADER} }
        RAND_LOGIN = self.rand_word_gen() + "@gmail.com"
        RAND_PASSWORD = self.rand_word_gen_range(start=10, end=30) + "A3!"

        return {
            "SERVICE": SERVICE,
            "TOKEN": TOKEN,
            "AUTH_TOKEN": AUTH_TOKEN,
            "SERVICE_NAME": SERVICE_NAME,
            "DEFAULT_HEADER": DEFAULT_HEADER,
            "CONTEXT_VALUE": CONTEXT_VALUE,
            "RAND_LOGIN": RAND_LOGIN,
            "RAND_PASSWORD": RAND_PASSWORD,
        }

    def create_account_for_test(self, email_verify: bool=True, status: str="ACTIVE", reg: str="APPROVED") -> tuple[dict,dict]:
        
        RAND_LOGIN = self.rand_word_gen() + "@gmail.com"
        RAND_PASSWORD = self.rand_word_gen_range(start=10, end=30) + "A3!"
        data = { "login": RAND_LOGIN, "password": RAND_PASSWORD }
        
        password_hash = self.hash_password(data["password"]).decode("utf-8")
        dateModified = str(datetime.utcnow())
        
        sql = text(f""" 
            INSERT INTO account_info(account_info_id,account_info_email,account_info_password,account_info_registered_on,account_info_verified_email,account_info_registration_status,account_info_status) 
            VALUES(nextval('account_info_sequence'),'{data["login"]}','{password_hash}','{dateModified}',{email_verify},'{reg}','{status}');

            INSERT INTO account_contact(account_contact_info_id) 
            VALUES(currval('account_info_sequence'));
            
            SELECT account_info_id,account_info_email,account_info_registration_status
            FROM account_info 
            WHERE account_info.account_info_email = '{data["login"]}'
        """)
                
        with self.db.get_engine("psqldb_movie").connect() as db:
            return self.list_sql_response(db, sql)[0], data
        
    def reset_database(self) -> None:
        sql = text(f"""
            DELETE FROM account_info;
            ALTER SEQUENCE account_info_sequence RESTART WITH 1;
            
            DELETE FROM account_contact;
            DELETE FROM account_archive;
            
            DELETE FROM movie_fav_info;
            ALTER SEQUENCE movie_fav_info_sequence RESTART WITH 1;
            
            DELETE FROM movie_imdb_info;
            ALTER SEQUENCE movie_imdb_info_sequence RESTART WITH 1;
            
        """)
        with self.db.get_engine("psqldb_movie").connect() as db:
            db.execute(sql)
        
    def delete_extra_account(self) -> None:
        with self.db.get_engine("psqldb_movie").connect() as db:
            sql = text(f"""
                DELETE 
                FROM account_info
                WHERE account_info_id > 1;
            """)
            db.execute(sql)
        
    def create_movie_fav(self, user_id: int) -> dict:
        movie_payload = {
            "movie_imdb_info_imdb_id": "0133093",
            "movie_imdb_info_title": "The Matrix",
            "movie_imdb_info_cast": ["test"],
            "movie_imdb_info_year": 1999,
            "movie_imdb_info_directors": ["test"],
            "movie_imdb_info_genres": ["test"],
            "movie_imdb_info_countries":["test"],
            "movie_imdb_info_plot": "test",
            "movie_imdb_info_cover": "test",
        }
        
        movieInput = {
            "movie_fav_info_imdb_id": "0133093",
            "movie_fav_info_episode_current": "1",
            "movie_fav_info_status": "completed",
            "movie_fav_info_rating_user": 9.8,
            "movie_fav_info_user_id": user_id,
        }
        
        request_key_imdb,request_val_imdb = self.request_fields(data=movie_payload)
        request_key,request_val = self.request_fields(data=movieInput)
        
        sql = text(f"""                   
            INSERT INTO movie_imdb_info(movie_imdb_info_id,{request_key_imdb})
            VALUES(nextval('movie_imdb_info_sequence'),{request_val_imdb});
            
            INSERT INTO movie_fav_info(movie_fav_info_id,{request_key}, movie_fav_info_imdb_info_id)
            VALUES(nextval('movie_fav_info_sequence'),{request_val}, currval('movie_imdb_info_sequence'));

            SELECT *
            FROM movie_fav_info
            INNER JOIN movie_imdb_info ON movie_imdb_info_id = movie_fav_info.movie_fav_info_imdb_info_id;
        """)
        
        with self.db.get_engine("psqldb_movie").connect() as db:
            return self.list_sql_response(db, sql)[0]