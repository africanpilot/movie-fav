# Copyright © 2022 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import os
import redis

from redis.client import Redis
from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlmodel import SQLModel, Session
from sqlalchemy.engine.base import Connection, Engine
from contextlib import contextmanager
from typing import Generator
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
				pool_pre_ping=True,  # Verify connections before use
				echo=False,  # Set to True for SQL debugging
			)

		if dbType == "redis":
			pool = redis.ConnectionPool.from_url(conn_url)
			engine = redis.Redis(connection_pool=pool, decode_responses=True)

		return engine

	def get_connection(self, *args) -> Connection:
		"""Get a raw SQLAlchemy connection. Use sparingly - prefer get_session()."""
		engine = self.get_engine(*args)
		return engine.connect()

	def get_session(self, *args) -> Session:
		"""Get a SQLModel session with proper configuration for SQLAlchemy 2.0+."""
		engine = self.get_engine(*args)
		return Session(engine, autocommit=False, autoflush=False)

	def get_redis_session(self, *args) -> Redis:
		return self.get_engine(*args, dbType="redis")

	@contextmanager
	def get_db_session(self, *args) -> Generator[Session, None, None]:
		"""Context manager for database sessions with automatic cleanup."""
		session = self.get_session(*args)
		try:
			yield session
			session.commit()
		except Exception:
			session.rollback()
			raise
		finally:
			session.close()

	@contextmanager
	def get_db_connection(self, *args) -> Generator[Connection, None, None]:
		"""Context manager for database connections with automatic cleanup."""
		connection = self.get_connection(*args)
		try:
			yield connection
		finally:
			connection.close()

	def create_db_and_tables(self, name):
		SQLModel.metadata.create_all(self.get_engine(f"psqldb_{name}"))
  
	def drop_db_and_tables(self, name):
		SQLModel.metadata.drop_all(self.get_engine(f"psqldb_{name}"), checkfirst=False)
  
	def create_default_schema(self):
		"""Create schemas for all enabled microservices using modern SQLAlchemy 2.0+ syntax."""
		engine = self.get_engine("psqldb_default")
		with engine.begin() as conn:
			for ms in self.general.enabled_microservices:
				if not conn.dialect.has_schema(conn, ms):
					conn.execute(CreateSchema(ms))
   
	def drop_default_schema(self):
		"""Drop schemas for all enabled microservices using modern SQLAlchemy 2.0+ syntax."""
		engine = self.get_engine("psqldb_default")
		with engine.begin() as conn:
			for ms in self.general.enabled_microservices:
				if conn.dialect.has_schema(conn, ms):
					conn.execute(DropSchema(ms, cascade=True))
			
	def create_database(self, name: str, models: list[SQLModel]):
		"""Create database tables for the given models using modern SQLAlchemy 2.0+ syntax."""
		engine = self.get_engine(f"psqldb_{name}")
		with engine.begin() as conn:
			for model in models:
				model.metadata.create_all(conn, checkfirst=True)

	def drop_database(self, name: str, models: list[SQLModel]):
		"""Drop database tables for the given models using modern SQLAlchemy 2.0+ syntax."""
		engine = self.get_engine(f"psqldb_{name}")
		with engine.begin() as conn:
			# Drop tables in reverse order to handle foreign key dependencies
			for model in reversed(models):
				model.metadata.drop_all(conn, checkfirst=True)
