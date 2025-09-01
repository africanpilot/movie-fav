# Database Fixtures - Migration to SQLAlchemy 2.0+

## Summary of Changes

This update migrates the database fixtures to use modern SQLAlchemy 2.0+ patterns and ensures proper database cleanup for pytest tests.

## Key Improvements

### 1. Modern SQLAlchemy 2.0+ Patterns

- **Connection Management**: Using `engine.begin()` context manager for automatic transaction handling
- **Session Configuration**: Properly configured sessions with `autocommit=False` and `autoflush=False`
- **Connection Pooling**: Added `pool_pre_ping=True` for better connection health checks
- **Type Hints**: Added proper type annotations for better IDE support

### 2. Robust Test Isolation

- **Function Scope**: All fixtures use `scope="function"` for proper test isolation
- **Transaction Management**: Proper transaction handling with automatic rollback on errors
- **Cleanup Guarantees**: Database is always cleaned up, even if tests fail
- **Exception Handling**: Robust error handling during setup and teardown

### 3. Multiple Fixture Options

#### `test_database`
- **Use Case**: Standard database testing with automatic cleanup
- **Features**: Transaction management, automatic rollback on errors, guaranteed cleanup
- **Best For**: Most test scenarios

#### `reset_database`
- **Use Case**: Mid-test database reset functionality
- **Features**: Function to reset database state during test execution
- **Best For**: Tests that need to simulate multiple scenarios

#### `clean_database`
- **Use Case**: Direct engine access with minimal overhead
- **Features**: Provides engine object for custom session management
- **Best For**: Performance-critical tests or custom session handling

#### `truncate_tables`
- **Use Case**: Fast data cleanup without dropping tables
- **Features**: Truncates all tables with CASCADE for foreign keys
- **Best For**: Tests that only need data cleanup, not schema changes

### 4. Improved Error Handling

- **Transaction Rollback**: Automatic rollback on test failures
- **Session Cleanup**: Guaranteed session closure
- **Exception Isolation**: Cleanup errors don't mask test failures
- **Database State**: Always ensures clean state for next test

## Usage Examples

### Basic Test
```python
def test_something(test_database: Session):
    # Add data
    user = User(name="John", email="john@example.com")
    test_database.add(user)
    test_database.commit()
    
    # Query data
    result = test_database.exec(select(User).where(User.email == "john@example.com")).first()
    assert result.name == "John"
    # Database automatically cleaned up after test
```

### Test with Reset
```python
def test_with_reset(test_database: Session, reset_database):
    # Add some data
    user = User(name="John", email="john@example.com")
    test_database.add(user)
    test_database.commit()
    
    # Reset database mid-test
    reset_database()
    
    # Database is now clean
    result = test_database.exec(select(User)).first()
    assert result is None
```

### Fast Cleanup Test
```python
def test_with_truncation(test_database: Session, truncate_tables):
    # Add data
    user = User(name="John", email="john@example.com")
    test_database.add(user)
    test_database.commit()
    
    # Fast cleanup (just data, not schema)
    truncate_tables()
    
    # Tables are empty but schema intact
    result = test_database.exec(select(User)).first()
    assert result is None
```

## Migration Notes

### Breaking Changes
- Fixture scope changed from default to explicit `function` scope
- Session handling is now more strict about transaction management
- Error handling is more robust but may expose previously hidden issues

### Benefits
- **Better Test Isolation**: Each test gets a completely clean database
- **Improved Reliability**: Robust error handling and cleanup
- **Modern Patterns**: Uses SQLAlchemy 2.0+ best practices
- **Performance Options**: Multiple fixtures for different performance needs
- **Type Safety**: Better type hints and IDE support

### Recommendations
1. **Use `test_database`** for most tests - it's the most robust option
2. **Use `truncate_tables`** for performance-critical test suites
3. **Use `reset_database`** when you need to simulate multiple scenarios in one test
4. **Use `clean_database`** when you need direct engine access

## Database Connection Improvements

The `DbConn` class has also been updated with:

- **Context Managers**: New `get_db_session()` and `get_db_connection()` methods
- **Modern Syntax**: Updated schema and table management methods
- **Better Error Handling**: Improved exception handling throughout
- **Connection Health**: Added `pool_pre_ping` for better connection reliability
