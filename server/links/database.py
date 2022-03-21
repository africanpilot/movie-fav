from sqlalchemy import create_engine
import urllib.parse
import os

class DbConn:
    def __init__(self):
        pass

    def get_engine(self,dbName):
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
                }
            }
        }

        cred = conn["db"]["postgresql"][dbName]
        password = urllib.parse.quote(cred['password'], safe='')
        SQLALCHEMY_DATABASE_URL = f"postgresql://{cred['user']}:{password}@{cred['host']}:{cred['port']}/{cred['database']}"

        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        return engine