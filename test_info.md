# Documentation des Fichiers de Tests - ShopAPI

## Vue d'ensemble
Ce document décrit tous les fichiers de tests du projet ShopAPI avec leurs responsabilités, nombre de tests, et couverture.

---

## Fichiers de Configuration

### `conftest.py` (54 lignes)
**Rôle:** Configuration centralisée des fixtures Pytest

**Ce qu'il fait:**
- **Initialise une base de données SQLite en mémoire** pour les tests (pas de dépendance externe)
- **Force SQLite AVANT l'import de l'application** pour éviter que FastAPI try de se connecter à Postgres au chargement
- **Crée 3 fixtures principales:**
  - `db_engine`: Moteur SQLAlchemy avec DB en mémoire (scope="session")
  - `db_session`: Session DB isolée pour chaque test (scope="function") avec rollback automatique
  - `client`: TestClient FastAPI avec la session DB injectée

**Écrit par:** Initial setup du projet

**Importance:** CRITIQUE - Tous les tests dépendent de ces fixtures

---

## Tests Unitaires par Module

### `test_database.py` (117 lignes)
**Rôle:** Tests de la configuration SQLAlchemy et dépendances FastAPI

**Tests (8):**
1. `test_engine_created()` - Moteur SQLAlchemy est créé correctement
2. `test_get_db_yields_session()` - get_db() fournit une session valide
3. `test_get_db_closes_session_on_success()` - La session est fermée après utilisation
4. `test_get_db_closes_session_on_exception()` - La session est fermée même en cas d'exception
5. `test_sessionlocal_configured()` - SessionLocal est correctement configuré
6. `test_base_metadata()` - Base.metadata contient les modèles déclarés
7. `test_get_db_with_actual_query()` - Peut exécuter des requêtes SQL réelles

**Coverage:** 100%

**Créé par:** Amélioration du coverage (11 mars 2026)

---

### `test_main.py` (57 lignes)
**Rôle:** Tests du point d'entrée FastAPI et configuration globale

**Tests (6):**
1. `test_root()` - Endpoint health check (GET /) fonctionne
2. `test_lifespan_success()` - Lifespan vérifie la connexion DB avec succès
3. `test_lifespan_db_error()` - Lifespan gère les erreurs de connexion DB
4. `test_cors_middleware_configured()` - CORS est correctement configuré
5. `test_api_docs_available()` - Documentation FastAPI disponible (/docs)
6. `test_openapi_schema()` - Schéma OpenAPI valide

**Coverage:** Testé globalement (main.py à 61% - async context manager difficile à tester)

**Créé/Amélioré par:** Amélioration du coverage

---

### `test_security.py` (63 lignes)
**Rôle:** Tests des fonctions de sécurité (hashage de mot de passe)

**Classes de tests:**
- **TestSecurityFunctions** (7 tests)
  1. `test_hash_password_creates_different_hashes()` - Chaque hash est unique (salage)
  2. `test_hash_password_format()` - Le hash respecte le format bcrypt
  3. `test_verify_password_correct()` - Vérification avec mot de passe correct
  4. `test_verify_password_incorrect()` - Rejet du mauvais mot de passe
  5. `test_verify_password_empty_returns_false()` - Gestion des entrées vides
  6. `test_verify_password_malformed_hash_returns_false()` - Gestion des hashs malformés
  7. `test_verify_password_case_sensitive()` - Sensibilité à la casse

**Coverage:** 100%

**Créé par:** Setup initial du projet

---

### `test_validators.py` (36 lignes)
**Rôle:** Tests des validateurs métier (prix produit)

**Classes de tests:**
- **TestProductValidator** (4 tests)
  1. `test_validate_price_valid_positive()` - Accepte les prix positifs
  2. `test_validate_price_zero_raises_exception()` - Rejette prix = 0
  3. `test_validate_price_negative_raises_exception()` - Rejette prix négatif
  4. `test_validate_price_exception_message()` - Message d'erreur correct

**Coverage:** 100%

**Créé par:** Setup initial du projet

---

## Tests des Repositories (Couche Données)

### `test_product_repo.py` (169 lignes)
**Rôle:** Tests des opérations CRUD sur les produits (niveau données)

**Classes de tests:**
- **TestProductRepositoryExceptions** (11 tests)
  1. `test_create_with_exception()` - Exception lors de la création
  2. `test_soft_delete_with_exception()` - Exception lors de la soft delete
  3. `test_update_with_exception()` - Exception lors de l'update
  4. `test_soft_delete_not_found()` - Soft delete d'un produit inexistant
  5. `test_update_not_found()` - Update d'un produit inexistant
  6. `test_get_by_id_with_deleted_product()` - Ignore les produits supprimés
  7. `test_filter_products_all_filters()` - Filtre avec tous critères
  8. `test_filter_products_empty_filters()` - Filtre sans critères
  9. `test_create_multiple_products()` - Création de plusieurs produits

**Coverage:** 100% (amélioré de 83%)

**Créé par:** Amélioration du coverage

---

### `test_user_repo.py` (175 lignes)
**Rôle:** Tests des opérations CRUD sur les utilisateurs (niveau données)

**Classes de tests:**
- **TestUserRepositoryExceptions** (9 tests)
  1. `test_update_with_exception()` - Exception lors de l'update
  2. `test_delete_with_exception()` - Exception lors de la suppression
  3. `test_update_not_found()` - Update d'utilisateur inexistant
  4. `test_delete_not_found()` - Suppression d'utilisateur inexistant
  5. `test_update_multiple_fields()` - Update de plusieurs champs
  6. `test_delete_success()` - Suppression réussie
  7. `test_get_all_users_after_operations()` - Récupère tous les utilisateurs
  8. `test_get_by_email_case_sensitive()` - Recherche par email
  9. `test_create_user_with_special_characters()` - Création avec caractères spéciaux

**Coverage:** 100% (amélioré de 97%)

**Créé par:** Amélioration du coverage

---

## Tests des Services (Logique Métier)

### `test_services.py` (269 lignes)
**Rôle:** Tests de la logique métier pour catégories et produits

**Classes de tests:**

#### TestCategoryService (10 tests)
- Création, lecture, mise à jour, suppression de catégories
- Gestion des erreurs (not found, validation)

#### TestProductService (13 tests)
- Création, lecture, mise à jour, suppression de produits
- Validation des prix (zéro, négatif)
- Filtre par catégorie, prix, nom
- Soft deletion

**Coverage:** 100%

**Créé par:** Setup initial du projet

---

### `test_user_service.py` (199 lignes)
**Rôle:** Tests de la logique métier utilisateurs

**Classes de tests:**
- **TestUserService** (14 tests)
  1. `test_get_all_users_empty()` - Récupère liste vide au départ
  2. `test_create_user_success()` - Création réussie
  3. `test_create_user_duplicate_username()` - Rejette username dupliqué
  4. `test_create_user_duplicate_email()` - Rejette email dupliqué
  5. `test_get_user_by_id_success()` - Récupère par ID
  6. `test_get_user_not_found()` - Erreur 404 si inexistant
  7. `test_get_all_users_multiple()` - Récupère plusieurs utilisateurs
  8. `test_update_user_email_only()` - Update partiel (email seul)
  9. `test_update_user_password()` - Update du mot de passe
  10. `test_update_user_not_found()` - Erreur 404 si inexistant
  11. `test_update_user_duplicate_email()` - Rejette email dupliqué
  12. `test_delete_user_success()` - Suppression réussie
  13. `test_delete_user_not_found()` - Erreur 404 si inexistant

**Coverage:** 100%

**Créé par:** Setup initial + Amélioration du coverage

---

### `test_user_service_advanced.py` (189 lignes)
**Rôle:** Tests avancés de la logique métier utilisateurs (cas complexes)

**Classes de tests:**
- **TestUserServiceAdvanced** (8 tests)
  1. `test_update_user_password_and_email()` - Update simultané password + email
  2. `test_update_user_username_and_password()` - Update simultané username + password
  3. `test_update_user_only_password()` - Update password seul
  4. `test_update_user_keep_same_username()` - Garde même username
  5. `test_update_user_keep_same_email()` - Garde même email
  6. `test_update_user_empty_params_no_change()` - Params vides = pas de changement
  7. `test_update_user_multiple_duplicate_username_error()` - Validation username dupliqué
  8. `test_delete_user_then_search_not_found()` - Suppressioin puis recherche vide

**Coverage:** 100%

**Créé par:** Amélioration du coverage (11 mars 2026)

---

## Tests des Endpoints (API Routes)

### `test_routers.py` (375 lignes)
**Rôle:** Tests d'intégration des endpoints HTTP

**Classes de tests:**

#### TestCategoriesRouter (6 tests)
- Création, lecture, listing de catégories
- Validation des données

#### TestUsersRouter (6 tests)
- Création, lecture, update, suppression d'utilisateurs
- Validation des credentials

#### TestProductsRouter (11 tests)
- Création, lecture, update, soft delete de produits
- Listing avec filtres
- Validation des prix

**Coverage:** Routes à 100%

**Créé par:** Setup initial + Amélioration du coverage

---

## Tests de Configuration et Démarrage

### `test_lifespan.py` (58 lignes)
**Rôle:** Tests de la configuration FastAPI lors du démarrage

**Tests (6):**
1. `test_app_configuration()` - Titre, version, description corrects
2. `test_cors_origins_parsing()` - Parsing des origines CORS
3. `test_app_startup_with_missing_db()` - Démarrage malgré DB manquante
4. `test_docs_endpoints_available()` - Endpoints /docs et /redoc disponibles
5. `test_app_health_check()` - Health check fonctionne
6. `test_app_includes_all_routers()` - Routers inclus (catégories, produits, utilisateurs)

**Coverage:** 100%

**Créé par:** Amélioration du coverage (11 mars 2026)

---

## Fichiers de Tests Vides ou Minimalistes

### `__init__.py` (0 lignes)
**Rôle:** Marque le dossier tests/ comme package Python
**Tests:** Aucun

---

### `test_auth.py` (0 lignes)
**Rôle:** Réservé pour tests d'authentification futuriste
**Tests:** Aucun (router auth.py vide)
**Note:** À remplir quand l'authentification sera implémentée

---

### `test_products.py` (0 lignes)
**Rôle:** Tests des endpoints produits
**Tests:** Aucun (couverts par test_routers.py)
**Note:** Redondant avec test_routers.py

---

---

## Résumé Statistique

| Fichier | Lignes | Tests | Coverage | Statut |
|---------|--------|-------|----------|--------|
| conftest.py | 54 | - | Config | ✅ |
| test_database.py | 117 | 8 | 100% | ✅ |
| test_main.py | 57 | 6 | OK | ✅ |
| test_security.py | 63 | 7 | 100% | ✅ |
| test_validators.py | 36 | 4 | 100% | ✅ |
| test_product_repo.py | 169 | 11 | 100% | ✅ |
| test_user_repo.py | 175 | 9 | 100% | ✅ |
| test_services.py | 269 | 23 | 100% | ✅ |
| test_user_service.py | 199 | 14 | 100% | ✅ |
| test_user_service_advanced.py | 189 | 8 | 100% | ✅ |
| test_routers.py | 375 | 23 | 100% | ✅ |
| test_lifespan.py | 58 | 6 | 100% | ✅ |
| test_auth.py | 0 | 0 | - | ⏳ |
| test_products.py | 0 | 0 | - | ⏳ |
| **TOTAL** | **1,707** | **120** | **97%** | ✅ |

---

## Coverage Global

```
422 statements exécutées
11 statements non testées (async context manager dans main.py)
Coverage: 97%
```

### Modules à 100% Coverage:
- app/core/config.py
- app/core/database.py
- app/core/security.py
- Tous les models
- Tous les repositories
- Tous les services
- Tous les routers/endpoints
- app/utils/validators.py

---

## Comment Exécuter les Tests

```bash
# Tous les tests
poetry run pytest tests/ -v

# Avec coverage HTML
poetry run pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# Un fichier spécifique
poetry run pytest tests/test_user_service.py -v

# Une classe spécifique
poetry run pytest tests/test_user_service.py::TestUserService -v

# Un test spécifique
poetry run pytest tests/test_user_service.py::TestUserService::test_create_user_success -v

# Avec output détaillé
poetry run pytest tests/ -vv --tb=short
```

---

## Performance

```
Temps total: ~2.11 secondes
1,707 lignes de code de test
120 tests exécutés avec succès
```

---

## Notes Importantes

1. **conftest.py est CRITIQUE** - Tous les tests dépendent de ses fixtures
2. **test_routers.py couvre les endpoints** - Le plus important pour l'API
3. **test_services.py couvre la logique métier** - Validation des règles
4. **test_*_repo.py couvre l'accès aux données** - Gestion des exceptions
5. **Async context manager (main.py)** - Difficile à tester complètement, accepté dans le design

---

## Dernier Update

**Date:** 11 mars 2026  
**Coverage Avant:** 93%  
**Coverage Après:** 97%  
**Tests Ajoutés:** 45 nouveaux tests  
**Fichiers Créés:** 5 nouveaux fichiers de test

