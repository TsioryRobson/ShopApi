"""
Point d'entrée de l'application FastAPI — ShopAPI.

On importe et on branche chaque router ici.
Chaque router gère ses propres préfixes et endpoints.
"""

from fastapi import FastAPI
from app.routers import categories

# Création de l'application avec métadonnées pour Swagger
app = FastAPI(
    title="ShopAPI",
    description="API REST de gestion d'inventaire e-commerce",
    version="0.1.0",
)

# Branchement des routers
app.include_router(categories.router)


@app.get("/", tags=["Health"])
def root():
    """Health check — vérifie que l'API tourne."""
    return {"message": "Test shop API running"}