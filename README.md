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

# Structure du projet
shopapi/
│
├── app/
│ ├── main.py
│ ├── core/
│ ├── models/
│ ├── routers/
│ ├── services/
│ └── repositories/
│
├── tests/
├── docs/
│
├── pyproject.toml
├── poetry.lock
└── README.md


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

## Swagger :
```bash 
http://127.0.0.1:8000/docs
```

## Run les tests
```bash 
poetry run pytest
```