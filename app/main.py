"""
Point d'entree de l'application FastAPI — ShopAPI.

Au demarrage, verifie la connexion DB.
Les tables sont gerees par Alembic (migrations versionnees).
Commande : poetry run alembic upgrade head
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.routers import categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Au demarrage : verifie la connexion a la DB."""
    try:
        from app.core.database import engine

        # Simple test de connexion — les tables sont gerees par Alembic
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[OK] Base de donnees connectee.")
        print("[INFO] Tables gerees par Alembic → 'poetry run alembic upgrade head'")
    except Exception as e:
        print(f"[WARN] Impossible de se connecter a la DB: {e}")
        print("[INFO] Lancez Docker : docker compose --env-file .env up postgres -d")
        print("[INFO] Puis appliquez les migrations : poetry run alembic upgrade head")
    yield


app = FastAPI(
    title="ShopAPI",
    description="API REST de gestion d'inventaire e-commerce",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(categories.router)


@app.get("/", tags=["Health"])
def root():
    """Health check — verifie que l'API tourne."""
    return {"message": "Test shop API running"}