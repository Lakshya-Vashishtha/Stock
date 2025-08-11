# migrations/env.py
import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Import your 'db' instance directly from 'app.extensions'.
# This is the most direct way for Alembic to get SQLAlchemy's metadata
# from your Flask application.
from app.extensions import db as application_db

# Import your models explicitly to ensure they are loaded into SQLAlchemy's metadata.
# Even though they are imported in __init__.py, explicitly importing them here
# ensures Alembic can discover them directly for autogenerate.
from app.models.User import User
from app.models.Business import Business
from app.models.products import Product

# from app.models.Inventory import Inventory


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


# Set target_metadata directly from your application's db instance.
# This ensures Alembic sees all models registered with your SQLAlchemy instance.
target_metadata = application_db.metadata


def get_engine():
    """
    Retrieves the SQLAlchemy engine from the current Flask application context.
    This function relies on Flask-Migrate having set up the app context.
    """
    try:
        # This works with Flask-SQLAlchemy < 3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # This works with Flask-SQLAlchemy >= 3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    """
    Generates the database URL string from the engine.
    """
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Set the database URL in the Alembic config.
    # This must be done inside run_migrations_online() because current_app
    # is guaranteed to be available here by Flask-Migrate.
    config.set_main_option('sqlalchemy.url', get_engine_url())

    # This callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema.
    # Reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    # Configure arguments for Alembic context, including the revision directive processor.
    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata, # Use the global target_metadata
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine whether to run migrations in offline or online mode.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
