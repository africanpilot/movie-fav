from sqlalchemy import create_engine
import urllib.parse
import os
import redis

class DbConn:
    def __init__(self):
        pass

    def get_engine(self, dbName, dbType="postgresql"):
        conn = {
            "db": {
                "postgresql": {
                    "psqldb_movie": {
                        "user": str(os.environ['DB_USERNAME']),
                        "password": str(os.environ['DB_PASSWORD']),
                        "host": str(os.environ['DB_LOCAL_HOST']),
                        "port": str(os.environ['DB_PORT']),
                        "database": str(os.environ['DB_DATABASE']),
                    }
                },
                "redis": {
                    "redisdb_movie": {
                        "password": str(os.environ['DB_REDIS_PASSWORD']),
                        "host": str(os.environ['DB_REDIS_HOST']), 
                        "port": str(os.environ['DB_REDIS_PORT']), 
                        "database": str(os.environ['DB_REDIS_DATABASE']),
                    }
                }
            }
        }
        
        cred = conn["db"][dbType][dbName]

        if dbType == "postgresql":
            password = urllib.parse.quote(cred['password'], safe='')
            SQLALCHEMY_DATABASE_URL = f"postgresql://{cred['user']}:{password}@{cred['host']}:{cred['port']}/{cred['database']}"
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
        if dbType == "redis":
            # connection pool
            pool = redis.ConnectionPool(
                host=cred["host"], 
                port=cred["port"], 
                db=cred["database"],
                password=cred["password"]       
            )
            engine = redis.Redis(connection_pool=pool, decode_responses=True)
            
            # engine = redis.Redis(
            #     host=cred["host"], 
            #     port=cred["port"], 
            #     db=cred["database"],
            #     password=cred["password"]     
            # )
        return engine