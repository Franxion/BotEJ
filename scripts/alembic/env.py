import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()

# Get the directory containing env.py
config_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add the project root directory to the Python path
sys.path.insert(0, config_dir)

# Now we can import our modules
from src.database import Base, DATABASE_URL
from src.db_models import *  # This imports all our models

# This is the Alembic Config object
config = context.config

# Set the database URL in the Alembic configuration
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set up target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    This creates a connection and binds the engine to it.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()