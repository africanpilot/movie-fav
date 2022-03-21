from app_lib.lib import Lib
from sqlalchemy.sql import text
from colorama import Fore

class ExampleHelloQuery:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def example_hello_query(self, info):
        
        lib = Lib()
        
        with lib.gen.db.get_engine("psqldb_movie").connect() as db:
            lib.gen.log.debug(f"Db Connection works!")
            return lib.example_response(info=info, db=db, pageInfo={}, filterInput={})