"""
Point d'entree de l'application FastAPI — ShopAPI.

Au demarrage, tente de creer les tables dans Postgres.
Si la DB n'est pas dispo (Docker pas lance), l'API demarre quand meme.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import categories, products, users


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

cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def root():
    """Health check — verifie que l'API tourne."""
    return {"message": "Test shop API running"}
