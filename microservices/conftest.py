# Copyright © 2025 by Richard Maku, Inc.
# All Rights Reserved. Proprietary and confidential.

import logging
import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Configure logging for pytest to suppress verbose output from third-party libraries."""
    
    # Set specific loggers to WARNING or ERROR level to suppress debug/info messages
    logging.getLogger("amqp").setLevel(logging.WARNING)
    logging.getLogger("amqp.channel").setLevel(logging.WARNING)
    logging.getLogger("kombu").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.WARNING)
    logging.getLogger("pika").setLevel(logging.WARNING)
    
    # RabbitMQ/AMQP related loggers
    logging.getLogger("rabbitmq").setLevel(logging.WARNING)
    
    # Other common noisy loggers during testing
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    # # Keep application loggers at INFO level or higher
    # logging.getLogger("microservices").setLevel(logging.INFO)
    
    yield
