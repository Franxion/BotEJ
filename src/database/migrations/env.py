import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Get the absolute path to the project root
# Starting from the current file (env.py) location:
# env.py is in src/database/migrations
# We need to go up three levels to reach the project root
current_dir = os.path.abspath(os.path.dirname(__file__))  # migrations folder
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

# Add project root to Python path
sys.path.insert(0, project_root)

# Now we can import our modules using the full path from the project root
from src.database.connection import Base, DATABASE_URL
from src.database.models import *  # This imports all our models

# Get Alembic Config object
config = context.config

# Set the database URL in the configuration
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Setup logging from configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set up target metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        configuration = {}

    connectable = engine_from_config(
        configuration,
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