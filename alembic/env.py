"""
Configuration Alembic pour ShopAPI.

Ce fichier connecte Alembic à :
- La config du projet (DATABASE_URL via app.core.config)
- Les modèles SQLAlchemy (Base.metadata via app.models.tables)

Chaque dev utilise SA propre DATABASE_URL (définie dans .env).
Les fichiers de migration sont partagés via Git → synchronisation entre devs.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ──────────────────────────────────────────────────────────────
# 1. Config Alembic (lecture de alembic.ini)
# ──────────────────────────────────────────────────────────────
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ──────────────────────────────────────────────────────────────
# 2. Connexion à la config du projet (DATABASE_URL depuis .env)
# ──────────────────────────────────────────────────────────────
# On importe la config Pydantic du projet pour récupérer DATABASE_URL
# → Chaque dev a sa propre URL dans .env, Alembic la lit automatiquement
from app.core.config import settings

# On écrase la valeur "sqlalchemy.url" du alembic.ini par celle du .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# ──────────────────────────────────────────────────────────────
# 3. Import des modèles pour l'autogenerate
# ──────────────────────────────────────────────────────────────
# IMPORTANT : on importe Base ET tables pour qu'Alembic "voie"
# tous les modèles (CategoryDB, ProductDB, UserDB)
from app.core.database import Base
import app.models.tables  # noqa: F401 — force l'import des modèles

# target_metadata = les tables connues de SQLAlchemy
# Alembic compare CE metadata avec la DB réelle pour détecter les différences
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Mode offline — génère du SQL sans se connecter à la DB.
    Utile pour review ou environnements sans accès DB.
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
    Mode online — se connecte à la DB et applique les migrations.
    C'est le mode utilisé par défaut (alembic upgrade head).
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
