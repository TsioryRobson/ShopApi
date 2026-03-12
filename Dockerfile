FROM python:3.12-slim

# Evite les fichiers .pyc et force l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer poetry
RUN pip install --no-cache-dir poetry

# Dossier de travail
WORKDIR /app

# Copier uniquement les fichiers de dépendances
COPY pyproject.toml poetry.lock* /app/

# Configurer poetry pour installer dans l'environnement global du container.
# NOTE: `poetry lock --no-update` n'existe pas sur certaines versions de Poetry
# (notamment Poetry 2.x). On utilise `poetry lock` simple.
RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --no-interaction --no-ansi --no-root

# Copier le reste du projet
COPY . /app

# Port FastAPI
EXPOSE 8000

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]