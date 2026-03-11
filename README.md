# Front ShopAPI

Interface React pour utiliser le backend `ShopApi` (FastAPI).

## Fonctionnalites

- Health check de l'API (`GET /`)
- CRUD Categories (`/categories`)
- CRUD Products (`/products`)
- CRUD Users (`/users`)

## Configuration

Par defaut, le frontend appelle l'API sur `http://127.0.0.1:8000`.

Pour changer l'URL backend, cree un fichier `.env` dans `front-shopapi/`:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Lancer en local

```bash
npm install
npm run dev
```

Le frontend sera disponible sur l'URL Vite (en general `http://127.0.0.1:5173`).

## Build production

```bash
npm run build
```
