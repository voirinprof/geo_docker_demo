# Image de base légère, avec Python 3.11
FROM python:3.11-slim

# Dépendances système nécessaires à GeoPandas (via GDAL)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgdal-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Dossier de travail dans le conteneur
WORKDIR /app

# On copie d'abord requirements.txt seul : Docker met cette étape en
# cache et ne réinstalle pas les dépendances si seul main.py change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le reste du projet
COPY . .

# Commande exécutée au démarrage du conteneur
CMD ["python", "main.py"]
