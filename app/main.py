"""
Point d'entree de l'application FastAPI — ShopAPI.

Au demarrage, verifie la connexion DB.
Les tables sont gerees par Alembic (migrations versionnees).
Commande : poetry run alembic upgrade head
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.routers import categories, products, users, auth


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

cors_origins = [
    origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def root():
    """Health check — verifie que l'API tourne."""
    return {"message": "Test shop API running"}
