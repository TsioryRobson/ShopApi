"""
Point d'entree de l'application FastAPI — ShopAPI.

Au demarrage, tente de creer les tables dans Postgres.
Si la DB n'est pas dispo (Docker pas lance), l'API demarre quand meme.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import categories, products


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Au demarrage : connecte la DB et cree les tables."""
    try:
        from app.core.database import engine
        from app.models.tables import Base
        Base.metadata.create_all(bind=engine)
        print("[OK] Base de donnees connectee, tables creees.")
    except Exception as e:
        print(f"[WARN] Impossible de se connecter a la DB: {e}")
        print("[INFO] Lancez Docker : docker compose --env-file .env up -d")
        print("[INFO] L'API demarre sans DB — le health check fonctionne.")
    yield


app = FastAPI(
    title="ShopAPI",
    description="API REST de gestion d'inventaire e-commerce",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(categories.router)
app.include_router(products.router)


@app.get("/", tags=["Health"])
def root():
    """Health check — verifie que l'API tourne."""
    return {"message": "Test shop API running"}
