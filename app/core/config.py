"""
Configuration de l'application — chargement des variables d'environnement.

Pydantic BaseSettings lit automatiquement le fichier .env
→ Plus besoin de os.getenv() partout, tout est centralisé ici.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application, lue depuis .env"""

    # Base de données — Postgres via Docker (docker-compose.yml)
    DATABASE_URL: str = (
        "postgresql://shopapi_user:shopapi_pass_dev@localhost:5433/shopapi_db"
    )

    # JWT (pour US5 - Gaëlle)
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Nom du projet
    PROJECT_NAME: str = "ShopAPI"

    # Frontend origins autorisees pour les appels navigateur (CORS)
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"

    class Config:
        env_file = ".env"
        extra = (
            "ignore"  # Ignore les variables .env supplémentaires (POSTGRES_USER, etc.)
        )


# Instance unique — on l'importe partout avec : from app.core.config import settings
settings = Settings()
