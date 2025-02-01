from logging.config import fileConfig
from sqlalchemy import create_engine  # Используем синхронный движок
from alembic import context
import sys
import os

# Добавляем путь к проекту
sys.path.append(os.getcwd())

# Импортируем Base
from bot.models.db import Base

# Конфигурация Alembic
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Подключение к базе данных (синхронный движок)
url = config.get_main_option("sqlalchemy.url")
engine = create_engine(url)

def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме."""
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск миграций в онлайн-режиме."""
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
