# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import pytest
from sqlalchemy import text
from sqlmodel import Session

from link_lib.microservice_to_postgres import DbConn

from account.src.models import ALL_MODELS as ACCOUNT_ALL_MODELS
from movie.src.models import ALL_MODELS as MOVIE_ALL_MODELS
from person.src.models import ALL_MODELS as PERSON_ALL_MODELS
from shows.src.models import ALL_MODELS as SHOWS_ALL_MODELS


ALL_MODELS = [
    *ACCOUNT_ALL_MODELS,
    *MOVIE_ALL_MODELS,
    *PERSON_ALL_MODELS,
    *SHOWS_ALL_MODELS,
]

get_db = DbConn()


@pytest.fixture(scope="function")
def test_database():
    """
    Database fixture that provides a clean database session for each test.
    Uses function scope to ensure isolation between tests.
    Handles proper setup, cleanup, and transaction rollback.
    """
    db_session = None
    try:
        # Setup: Create schema and tables
        get_db.create_default_schema()
        get_db.create_database("default", ALL_MODELS)
        
        # Create session with autocommit=False for proper transaction handling
        engine = get_db.get_engine("psqldb_default")
        db_session = Session(engine, autocommit=False, autoflush=False)
        
        # Begin a transaction
        db_session.begin()
        
        yield db_session
        
    except Exception as e:
        # If there's an exception during test, rollback the transaction
        if db_session and db_session.in_transaction():
            db_session.rollback()
        raise e
        
    finally:
        # Cleanup: Always close session and clean database
        if db_session:
            try:
                # Rollback any pending transaction
                if db_session.in_transaction():
                    db_session.rollback()
            except Exception:
                pass  # Ignore rollback errors during cleanup
            finally:
                # Close the session
                db_session.close()
        
        # Clean up database tables and schema
        try:
            get_db.drop_database("default", ALL_MODELS)
            get_db.drop_default_schema()
        except Exception:
            pass  # Ignore cleanup errors to avoid masking test failures


@pytest.fixture(scope="function")
def reset_database():
    """
    Fixture that provides a function to reset the database state.
    Useful for tests that need to clean and reinitialize the database mid-test.
    """
    def reset_db():
        try:
            get_db.drop_database("default", ALL_MODELS)
            get_db.drop_default_schema()
        except Exception:
            pass  # Ignore errors during cleanup
        
        get_db.create_default_schema()
        get_db.create_database("default", ALL_MODELS)
    
    return reset_db


@pytest.fixture(scope="function")
def clean_database():
    """
    Alternative fixture that provides a clean database without automatic cleanup.
    Use this when you need more control over the database lifecycle.
    """
    try:
        # Setup
        get_db.create_default_schema()
        get_db.create_database("default", ALL_MODELS)
        
        engine = get_db.get_engine("psqldb_default")
        
        yield engine
        
    finally:
        # Cleanup
        try:
            get_db.drop_database("default", ALL_MODELS)
            get_db.drop_default_schema()
        except Exception:
            pass


@pytest.fixture(scope="function")
def truncate_tables():
    """
    Fixture that provides a function to truncate all tables.
    Faster than dropping/creating tables when you just need to clear data.
    """
    def truncate_all():
        engine = get_db.get_engine("psqldb_default")
        with Session(engine) as session:
            try:
                # Disable foreign key checks temporarily
                session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
                
                # Get all table names
                for model in ALL_MODELS:
                    table_name = model.__tablename__
                    session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"))
                
                # Re-enable foreign key checks
                session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
                session.commit()
                
            except Exception as e:
                session.rollback()
                # For PostgreSQL, use different syntax
                try:
                    for model in ALL_MODELS:
                        table_name = model.__tablename__
                        session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"))
                    session.commit()
                except Exception:
                    session.rollback()
                    raise e
    
    return truncate_all
