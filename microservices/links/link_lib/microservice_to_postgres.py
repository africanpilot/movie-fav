# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
import redis

from redis.client import Redis
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlmodel import SQLModel, Session
from sqlalchemy.engine.base import Connection
from link_lib.microservice_generic_model import GenericLinkModel


class DbConn:
	def __init__(self):
		pass
	
	@property
	def general(self):
		return GenericLinkModel()
			
	def get_engine(self, dbName: str, dbType: str = "postgresql") -> object:
		conn = {
			"db": {
				"postgresql": { 
					f"psqldb_{ms}": os.getenv(f"DB_POSTGRES_{ms.upper()}") 
					for ms in self.general.enabled_microservices
				},
				"redis": {
					f"redisdb_{ms}": os.getenv(f"DB_REDIS_{ms.upper()}") 
					for ms in self.general.enabled_microservices
				},
			}
		}
		
		conn["db"]["postgresql"].update({"psqldb_default": os.getenv("DB_POSTGRES_DEFAULT")})
		conn["db"]["redis"].update({"redisdb_default": os.getenv("DB_REDIS_DEFAULT")})		

		conn_url = conn["db"][dbType][dbName]

		if dbType == "postgresql":
			SQLALCHEMY_DATABASE_URL = conn_url
			engine = create_engine(
				url=SQLALCHEMY_DATABASE_URL,
				pool_size=20,
				max_overflow=0,
				pool_recycle=3600,
			)

		if dbType == "redis":
			pool = redis.ConnectionPool.from_url(conn_url)
			engine = redis.Redis(connection_pool=pool, decode_responses=True)

		return engine

	def get_connection(self, *args) -> Connection:
		return self.get_engine(*args).connect()

	def get_session(self, *args) -> Session:
		return Session(self.get_engine(*args))

	def get_redis_session(self, *args) -> Redis:
		return self.get_engine(*args, dbType="redis")

	def create_db_and_tables(self, name):
		SQLModel.metadata.create_all(self.get_engine(f"psqldb_{name}"))
  
	def drop_db_and_tables(self, name):
		SQLModel.metadata.drop_all(self.get_engine(f"psqldb_{name}"), checkfirst=False)
  
	def create_default_schema(self):
		with self.get_engine(f"psqldb_default").connect() as db:
			for ms in self.general.enabled_microservices:
				if not db.dialect.has_schema(db, ms):
					db.execute(CreateSchema(ms))
			db.commit()
   
	def drop_default_schema(self):
		with self.get_engine(f"psqldb_default").connect() as db:
			for ms in self.general.enabled_microservices:
				if db.dialect.has_schema(db, ms):
					db.execute(DropSchema(ms))
			db.commit()
			
	def create_database(self, name: str, models: list[SQLModel]):
		with self.get_engine(f"psqldb_{name}").connect() as db:
			for model in models:
				model.metadata.create_all(db, checkfirst=True)
			db.commit()

	def drop_database(self, name: str, models: list[SQLModel]):
		with self.get_engine(f"psqldb_{name}").connect() as db:
			for model in reversed(models):
				model.metadata.drop_all(db, checkfirst=True)
