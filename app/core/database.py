"""
Configuration SQLAlchemy — connexion a la base de donnees.

Ce fichier cree :
- engine       → le moteur de connexion (se connecte a Postgres)
- SessionLocal → la fabrique de sessions (1 session = 1 transaction)
- Base         → la classe mere de tous les modeles SQLAlchemy
- get_db()     → dependance FastAPI qui ouvre/ferme une session proprement
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Moteur de connexion — utilise DATABASE_URL du .env
# pool_pre_ping=True → verifie la connexion avant chaque requete
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Fabrique de sessions — chaque requete API recoit sa propre session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modeles SQLAlchemy (les tables)
Base = declarative_base()


def get_db():
    """
    Dependance FastAPI — fournit une session DB a chaque requete.

    Utilisation dans un router :
        @router.get("/")
        def list_items(db: Session = Depends(get_db)):
            ...

    La session est automatiquement fermee apres la requete (meme si erreur).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
