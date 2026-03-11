# ShopAPI

API REST simple de gestion d’inventaire e-commerce développée avec **FastAPI**.  
Le projet utilise **Poetry** pour la gestion des dépendances et de l’environnement.

---

# Stack technique

- **FastAPI** — Framework API
- **Uvicorn** — Serveur ASGI
- **Pydantic** — Validation des données
- **SQLAlchemy** — ORM base de données
- **Python-JOSE** — Authentification JWT
- **Pytest** — Tests
- **Black / Flake8 / Mypy** — Qualité du code
- **Poetry** — Gestion des dépendances

---

# Installation et run du procjet

```bash 
git clone <repo-url>
cd shopapi
```

## Installer les dépendances
```bash 
pip install poetry
```

## Lancer l’API
```bash 
poetry run uvicorn app.main:app --reload
```

## API disponible sur :
```bash 
http://127.0.0.1:8000
```

## CORS (acces navigateur)

Pour autoriser le frontend (Vite), configure `CORS_ORIGINS` dans `.env`.

Exemple:
```bash
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Pour plusieurs interfaces, ajoute les URLs separees par des virgules.

## Swagger :
```bash 
http://127.0.0.1:8000/docs
```

## Run les tests
```bash 
poetry run pytest
```
