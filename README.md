# geo-docker-demo

Petit projet pour illustrer les principes de base de Docker appliqués à
la géomatique : un script Python (GeoPandas) qui charge des polygones,
les reprojette et calcule leur superficie — le tout exécuté dans un
conteneur, sans rien installer sur la machine hôte.

## Contenu du dépôt

```
geo-docker-demo/
├── Dockerfile          ← définit l'image (Python + GDAL + GeoPandas)
├── .dockerignore        ← fichiers exclus du build
├── requirements.txt     ← dépendances Python
├── main.py               ← script d'exemple
├── data/
│   └── secteurs.geojson  ← données simplifiées, à but pédagogique
└── README.md
```

## Prérequis

Docker installé sur votre poste (Docker Desktop sur Windows/macOS,
Docker Engine sur Linux). Vérifiez avec :

```bash
docker --version
```

## Utiliser le projet dans GitHub Codespaces

GitHub Codespaces fournit un environnement de développement dans le
navigateur avec Docker déjà disponible. Pour lancer ce projet :

1. Sur GitHub, ouvrez la page du dépôt, cliquez sur **Code**, puis sur
  l'onglet **Codespaces**.
2. Cliquez sur **Create codespace on main** (ou choisissez la branche à
  utiliser). Attendez que le Codespace soit entièrement démarré.
3. Dans le terminal intégré de VS Code, vérifiez que Docker est
  disponible :

  ```bash
  docker --version
  ```

4. Construisez l'image depuis la racine du dépôt :

  ```bash
  docker build -t geo-docker-demo .
  ```

5. Exécutez l'exemple :

  ```bash
  docker run --rm geo-docker-demo
  ```

Les fichiers du dépôt sont directement accessibles dans le Codespace.
Les modifications sont conservées dans le Codespace et peuvent être
enregistrées avec Git puis envoyées sur GitHub avec `git add`, `git
commit` et `git push`. Pour éviter de consommer des ressources, arrêtez
ou supprimez le Codespace depuis **GitHub > Settings > Codespaces** quand
vous avez terminé (vous pouvez aussi visiter le lien suivant : https://github.com/codespaces, vous y verrez tous les environnements qui tournent.)

## Commandes de base

### 1. Construire l'image

```bash
docker build -t geo-docker-demo .
```

- `-t geo-docker-demo` donne un nom (tag) à l'image, pour la retrouver
  facilement ensuite
- Le `.` indique que le Dockerfile se trouve dans le dossier courant

### 2. Lancer un conteneur à partir de l'image

```bash
docker run --rm geo-docker-demo
```

- `--rm` supprime le conteneur automatiquement une fois l'exécution
  terminée (il n'a pas besoin de rester après coup)
- Le script `main.py` s'exécute et affiche les superficies calculées

### 3. Monter un dossier local (volume)

Pour que le conteneur utilise vos propres données, sans les copier
dans l'image :

```bash
docker run --rm -v "$(pwd)/data:/app/data" geo-docker-demo
```

- `-v hôte:conteneur` relie un dossier de votre machine à un dossier
  du conteneur — modifier `data/secteurs.geojson` localement change
  ce que le script lit, sans reconstruire l'image

### 4. Ouvrir un terminal dans le conteneur

Utile pour explorer l'environnement ou déboguer :

```bash
docker run --rm -it geo-docker-demo bash
```

- `-it` rend la session interactive (clavier + terminal)
- `bash` remplace la commande par défaut (`python main.py`) par un
  shell

### 5. Lister, inspecter, nettoyer

```bash
docker images              # images construites localement
docker ps                  # conteneurs en cours d'exécution
docker ps -a                # tous les conteneurs, y compris arrêtés
docker rmi geo-docker-demo  # supprimer l'image
docker system prune         # nettoyer les images/conteneurs inutilisés
```

## Modifier le projet

Après toute modification de `main.py` ou de `data/secteurs.geojson`,
il faut reconstruire l'image pour que le changement soit pris en
compte à l'intérieur du conteneur :

```bash
docker build -t geo-docker-demo .
docker run --rm geo-docker-demo
```

(Si vous utilisez un volume comme à l'étape 3, seules les
modifications du **code** nécessitent une reconstruction — les
données montées en volume sont toujours lues à jour.)

## Pourquoi Docker ici ?

`geopandas` dépend de GDAL, une bibliothèque système parfois délicate
à installer (versions incompatibles, dépendances manquantes selon le
système d'exploitation). Le `Dockerfile` fixe cet environnement une
fois pour toutes : le projet tourne à l'identique sur n'importe quel
poste ayant Docker installé, sans étape d'installation manuelle.
