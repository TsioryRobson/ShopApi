# 🛒 ShopAPI

API REST de gestion d'inventaire e-commerce développée avec **FastAPI**.  
Le projet utilise **Poetry** pour les dépendances, **Alembic** pour les migrations DB, et **Docker** pour PostgreSQL.

---

## 📋 Stack technique

| Outil | Rôle |
|-------|------|
| **FastAPI** | Framework API REST |
| **Uvicorn** | Serveur ASGI |
| **Pydantic** | Validation des données |
| **SQLAlchemy** | ORM base de données |
| **Alembic** | Migrations de base de données |
| **PostgreSQL** | Base de données (via Docker) |
| **Python-JOSE** | Authentification JWT |
| **Pytest** | Tests |
| **Black / Flake8 / Mypy** | Qualité du code |
| **Poetry** | Gestion des dépendances |

---

## 🚀 Installation (première fois)

### Prérequis
- **Python 3.12+**
- **Docker Desktop** (pour PostgreSQL)
- **Poetry** (`pip install poetry`)

### Étapes

```bash
# 1. Cloner le repo
git clone <repo-url>
cd ShopApi

# 2. Installer les dépendances
poetry install

# 3. Créer le fichier .env à partir de l'exemple
cp .env.example .env
# → Modifier les valeurs si nécessaire (ports, mots de passe...)

# 4. Lancer PostgreSQL via Docker
docker compose --env-file .env up postgres -d

# 5. Appliquer les migrations (créer les tables)
poetry run alembic upgrade head

# 6. Lancer l'API
poetry run uvicorn app.main:app --reload

docker compose build --no-cache api
docker compose up -d
```

### Accès
- **API** : http://127.0.0.1:8000
- **Swagger (docs)** : http://127.0.0.1:8000/docs
- **ReDoc** : http://127.0.0.1:8000/redoc

---

## 🗄️ Migrations avec Alembic

### Pourquoi Alembic ?

Alembic remplace `Base.metadata.create_all()` et permet de :
- **Versionner** les changements de la DB (comme Git pour le code)
- **Synchroniser** les schémas entre tous les devs
- **Rollback** si besoin (revenir à une version précédente)
- **Collaborer** sans conflits sur la structure de la DB

### Comment ça marche ?

```
Modèles SQLAlchemy (app/models/tables.py)
         │
         ▼
   alembic revision --autogenerate
         │
         ▼
Fichier de migration (alembic/versions/xxxx_description.py)
         │
         ▼
   alembic upgrade head
         │
         ▼
   Tables dans PostgreSQL
```

### Commandes essentielles

| Commande | Quand l'utiliser |
|----------|-----------------|
| `poetry run alembic upgrade head` | **À chaque `git pull`** — applique les nouvelles migrations |
| `poetry run alembic revision --autogenerate -m "description"` | Après avoir modifié un modèle dans `tables.py` |
| `poetry run alembic downgrade -1` | Revenir à la migration précédente |
| `poetry run alembic current` | Voir la migration actuelle de ta DB |
| `poetry run alembic history` | Voir l'historique des migrations |

### Workflow quotidien (pour chaque dev)

```bash
# 1. Tu pull les derniers changements
git pull origin develop

# 2. Tu appliques les nouvelles migrations (s'il y en a)
poetry run alembic upgrade head

# 3. Tu travailles normalement sur ton code...

# 4. Si TU modifies un modèle dans tables.py :
poetry run alembic revision --autogenerate -m "ajout_colonne_prix_promo"

# 5. Tu vérifies le fichier généré dans alembic/versions/
#    → Vérifie que le upgrade() et downgrade() sont corrects !

# 6. Tu appliques TA migration
poetry run alembic upgrade head

# 7. Tu commit tout (code + fichier de migration)
git add .
git commit -m "feat: ajout colonne prix_promo"
git push
```

## CORS (acces navigateur)

Pour autoriser le frontend (Vite), configure `CORS_ORIGINS` dans `.env`.

Exemple:
```bash
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Pour plusieurs interfaces, ajoute les URLs separees par des virgules.
```

### ⚠️ Règles importantes

1. **NE JAMAIS modifier un fichier de migration déjà pushé** — créer une nouvelle migration à la place
2. **NE JAMAIS supprimer les fichiers de migration** — ils constituent l'historique
3. **TOUJOURS** faire `alembic upgrade head` après un `git pull`
4. **TOUJOURS** vérifier le fichier généré avant de commit (parfois l'autogenerate se trompe)
5. **NE PAS** utiliser `Base.metadata.create_all()` — c'est Alembic qui gère les tables

---

## 🐳 Docker

### Commandes Docker

```bash
# Lancer PostgreSQL uniquement
docker compose --env-file .env up postgres -d

# Lancer tout (API + PostgreSQL)
docker compose --env-file .env up -d

# Voir les logs
docker compose logs -f

# Arrêter tout
docker compose down

# Arrêter et supprimer les données (reset complet)
docker compose down -v
```

### Connexion à la DB

```bash
# Depuis un outil (DBeaver, pgAdmin, DataGrip...)
Host: localhost
Port: 5434
User: shopapi_user
Password: shopapi_pass_dev
Database: shopapi_db
```

---

## Tests

```bash
# 1) Verifier/installer les dependances de test (passlib inclus)
make test-setup

# 2) Lancer tous les tests
make test

# 3) Lancer rapidement (sortie concise)
make test-fast

# 4) Lancer avec coverage + rapport HTML
make test-cov

# 5) Lancer un fichier cible
bash tests/run_tests.sh tests/test_auth.py -q
```

Important:
Ne pas lancer `pytest tests/conftest.py` directement.
`conftest.py` est un fichier de fixtures charge automatiquement par pytest.
Utiliser toujours `pytest tests` (ou `make test*`).

---

## 🔧 Qualité du code

```bash
# Formatter le code avec Black
poetry run black app/ tests/

# Linter avec Flake8
poetry run flake8 app/ tests/

# Vérification des types avec Mypy
poetry run mypy app/
```

---

## 📁 Structure du projet

```
ShopApi/
├── alembic/                   # Migrations de base de données
│   ├── versions/              # Fichiers de migration (versionnés par Git)
│   ├── env.py                 # Config Alembic (lit DATABASE_URL depuis .env)
│   └── script.py.mako         # Template des migrations
├── alembic.ini                # Configuration Alembic
├── app/
│   ├── core/
│   │   ├── config.py          # Variables d'environnement (Pydantic Settings)
│   │   ├── database.py        # Engine SQLAlchemy, Session, Base
│   │   ├── exceptions.py      # Exceptions métier
│   │   └── security.py        # Hashing, JWT
│   ├── models/
│   │   ├── tables.py          # Modèles SQLAlchemy (les TABLES)
│   │   ├── category.py        # Schémas Pydantic — Catégories
│   │   ├── product.py         # Schémas Pydantic — Produits
│   │   └── user.py            # Schémas Pydantic — Utilisateurs
│   ├── repositories/          # Accès DB (requêtes SQLAlchemy)
│   ├── services/              # Logique métier
│   ├── routers/               # Endpoints FastAPI
│   └── main.py                # Point d'entrée de l'application
├── tests/                     # Tests unitaires
├── docker-compose.yml         # Docker (PostgreSQL + API)
├── Dockerfile                 # Image Docker de l'API
├── pyproject.toml             # Dépendances (Poetry)
├── .env                       # Variables locales (NON versionné)
└── .env.example               # Template des variables d'environnement
```

---

## 🏷️ Branches Git

| Branche | Rôle |
|---------|------|
| `main` | Production — code stable uniquement |
| `develop` | Intégration — les features mergent ici |
| `feature/database-setup` | Setup DB + Alembic (Tsiory) |
| `feature/US1-crud-categories` | CRUD Catégories |
| `feature/Docker-config` | Configuration Docker |
| `features/US2_crud_products` | CRUD Produits (Dania) |
| `init/structure_project` | Structrue du projet (Dania) |
| `feature/front-shopapi` | Interface ( Manoa ) |
| `feature/us4_filtreproduitcategorie` | filtrage ( Daddy ) |
| `feature/ci-cd` | Teste Ci-Cd ( El-Nadje ) |
| `fix/get_product_by_id` | Interface ( Dania ) |
| `feature/US-5-auth-api` | Authentification-api ( Tsiory ) |
| `feature/add_mkDoks` | Documentation finale du projet ( Dania ) |
| `feature/us3-crud-user` | CRUD user ( Manoa) |
| `feature/majreadme` | Mise à jour du fichier Readme |

---

## ❓ Dépannage

### "Target database is not up to date"
```bash
# Applique d'abord les migrations en attente
poetry run alembic upgrade head
# Puis génère ta nouvelle migration
poetry run alembic revision --autogenerate -m "description"
```

### "Can't locate revision"
```bash
# Vérifie l'état actuel
poetry run alembic current
poetry run alembic history

# Si la DB est désynchronisée, stamp la version actuelle
poetry run alembic stamp head
```

### "Connection refused" à PostgreSQL
```bash
# Vérifie que Docker tourne
docker ps

# Relance PostgreSQL
docker compose --env-file .env up postgres -d

# Vérifie le port dans .env (doit être 5434 en local)
```
